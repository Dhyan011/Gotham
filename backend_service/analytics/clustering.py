"""
GOTHAM DBSCAN Hotspot Detection
Identifies spatial crime clusters using density-based clustering.
Returns GeoJSON FeatureCollection for map rendering.
"""
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
from database import SessionLocal, CaseMaster


def detect_hotspots(crime_type=None, date_from=None, date_to=None, district=None,
                    eps=0.05, min_samples=5):
    """
    Run DBSCAN on FIR lat/lng coordinates to identify crime hotspots.
    
    Criminology insight: DBSCAN is ideal for crime clustering because:
    - It doesn't require pre-specifying the number of clusters
    - It can find irregularly shaped clusters (crime doesn't follow circles)
    - It identifies noise points (isolated incidents vs. hotspot patterns)
    
    Parameters:
        eps: Maximum distance between two points to be in the same cluster.
             0.05 degrees ≈ 5.5km at Karnataka's latitude.
        min_samples: Minimum incidents to form a cluster.
    """
    db = SessionLocal()
    try:
        query = db.query(CaseMaster)
        if crime_type:
            query = query.filter(CaseMaster.crime_type == crime_type)
        if date_from:
            query = query.filter(CaseMaster.date_of_occurrence >= date_from)
        if date_to:
            query = query.filter(CaseMaster.date_of_occurrence <= date_to)
        if district:
            from database import Unit
            unit_ids = [u.unit_id for u in db.query(Unit).filter(Unit.district == district).all()]
            if unit_ids:
                query = query.filter(CaseMaster.unit_id.in_(unit_ids))

        cases = query.all()
    finally:
        db.close()

    if len(cases) < min_samples:
        return {"type": "FeatureCollection", "features": []}

    coords = np.array([[float(c.lat), float(c.lng)] for c in cases])
    severities = np.array([c.severity_weight or 1 for c in cases])
    crime_types = [c.crime_type for c in cases]
    mo_tags_all = [c.mo_tags or [] for c in cases]

    # Run DBSCAN
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine')
    # Convert to radians for haversine metric
    coords_rad = np.radians(coords)
    labels = clustering.fit_predict(coords_rad)

    # Build GeoJSON features for each cluster
    features = []
    unique_labels = set(labels)
    unique_labels.discard(-1)  # Remove noise label

    for cluster_id in unique_labels:
        mask = labels == cluster_id
        cluster_coords = coords[mask]
        cluster_severities = severities[mask]
        cluster_crimes = [crime_types[i] for i, m in enumerate(mask) if m]
        cluster_mo = []
        for i, m in enumerate(mask):
            if m:
                cluster_mo.extend(mo_tags_all[i])

        centroid_lat = float(np.mean(cluster_coords[:, 0]))
        centroid_lng = float(np.mean(cluster_coords[:, 1]))
        avg_severity = float(np.mean(cluster_severities))
        incident_count = int(mask.sum())

        # Dominant crime type in cluster
        from collections import Counter
        crime_counts = Counter(cluster_crimes)
        dominant_crime = crime_counts.most_common(1)[0][0] if crime_counts else "Unknown"
        top_mo = [tag for tag, _ in Counter(cluster_mo).most_common(3)]

        # Compute convex hull polygon for cluster boundary
        polygon_coords = []
        if len(cluster_coords) >= 3:
            try:
                hull = ConvexHull(cluster_coords)
                for idx in hull.vertices:
                    polygon_coords.append([
                        float(cluster_coords[idx][1]),  # GeoJSON: [lng, lat]
                        float(cluster_coords[idx][0])
                    ])
                polygon_coords.append(polygon_coords[0])  # Close the ring
            except Exception:
                # Fallback: bounding box
                min_lat, max_lat = float(cluster_coords[:, 0].min()), float(cluster_coords[:, 0].max())
                min_lng, max_lng = float(cluster_coords[:, 1].min()), float(cluster_coords[:, 1].max())
                polygon_coords = [
                    [min_lng, min_lat], [max_lng, min_lat],
                    [max_lng, max_lat], [min_lng, max_lat],
                    [min_lng, min_lat]
                ]
        else:
            # Too few points for hull, create a small box around centroid
            d = 0.01
            polygon_coords = [
                [centroid_lng - d, centroid_lat - d], [centroid_lng + d, centroid_lat - d],
                [centroid_lng + d, centroid_lat + d], [centroid_lng - d, centroid_lat + d],
                [centroid_lng - d, centroid_lat - d]
            ]

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            },
            "properties": {
                "cluster_id": int(cluster_id),
                "crime_type": dominant_crime,
                "incident_count": incident_count,
                "avg_severity": round(avg_severity, 2),
                "centroid_lat": centroid_lat,
                "centroid_lng": centroid_lng,
                "top_mo_tags": top_mo
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "data_source": "GOTHAM Synthetic Dataset v1.0 — Simulated for demonstration purposes",
            "algorithm_used": f"DBSCAN (eps={eps}, min_samples={min_samples})",
            "total_clusters": len(features),
            "total_incidents_analyzed": len(cases)
        }
    }


if __name__ == "__main__":
    result = detect_hotspots()
    print(f"Detected {len(result['features'])} hotspot clusters")
    for f in result["features"]:
        p = f["properties"]
        print(f"  Cluster {p['cluster_id']}: {p['incident_count']} incidents, "
              f"{p['crime_type']}, severity {p['avg_severity']}")

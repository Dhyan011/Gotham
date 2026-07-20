from sklearn.ensemble import IsolationForest
import numpy as np

def detect_multi_signal_anomaly(features, graph_degree_spike):
    """
    Multi-signal anomaly detection.
    features: List of numerical features per entity [z_score, other_metric]
    graph_degree_spike: list of spike values
    """
    if not features:
        return []
        
    X = np.array(features)
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X)
    predictions = clf.predict(X)
    
    anomalies = []
    for i, (pred, spike) in enumerate(zip(predictions, graph_degree_spike)):
        # Isolation Forest returns -1 for anomalies
        iso_score = 1.0 if pred == -1 else 0.0
        
        # Weighted fusion: Isolation Forest 60%, Graph Spike 40%
        fusion_score = (iso_score * 0.6) + (min(spike / 10.0, 1.0) * 0.4)
        
        if fusion_score > 0.5:
            anomalies.append({
                "entity_index": i,
                "fusion_score": round(fusion_score, 2),
                "isolation_anomaly": pred == -1,
                "graph_spike": spike
            })
            
    return anomalies

if __name__ == "__main__":
    pass

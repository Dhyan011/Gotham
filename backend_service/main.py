from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_parser import get_district_map_data
from anomaly_parser import get_anomaly_data

app = FastAPI(title="GOTHAM - Data-Driven Scope")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/map/districts")
def get_map_data():
    """
    Returns Phase 1 Geospatial District data derived directly from the real CSV.
    """
    data = get_district_map_data()
    return {"status": "success", "data": data, "count": len(data)}

@app.get("/api/stats/anomalies")
def get_anomalies():
    """
    Returns Phase 2 & 4 Anomalies calculated statistically from the real CSV.
    """
    anomalies = get_anomaly_data()
    return {"status": "success", "anomalies": anomalies, "count": len(anomalies)}

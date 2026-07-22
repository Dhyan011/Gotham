from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db
from analytics.alerts import get_alerts

router = APIRouter()

@router.get("/api/alerts")
def fetch_alerts(db: Session = Depends(get_db)):
    alerts = get_alerts(db)
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "alerts": alerts
    }

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db, CaseMaster, Unit

router = APIRouter()

@router.get("/api/hotspots")
def get_hotspots(
    crime_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CaseMaster, Unit).join(Unit, CaseMaster.unit_id == Unit.unit_id)
    
    if crime_type:
        query = query.filter(CaseMaster.crime_type == crime_type)
    if date_from:
        query = query.filter(CaseMaster.date_of_occurrence >= date_from)
    if date_to:
        query = query.filter(CaseMaster.date_of_occurrence <= date_to)
    if district:
        query = query.filter(Unit.district == district)
        
    cases = query.all()
    
    # Just returning coordinates for hotspots clustering on frontend
    points = [{"lat": float(c.CaseMaster.lat), "lng": float(c.CaseMaster.lng), "weight": c.CaseMaster.severity_weight} for c in cases if c.CaseMaster.lat and c.CaseMaster.lng]
    
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "hotspots": points
    }

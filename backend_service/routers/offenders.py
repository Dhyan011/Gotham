from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db, Accused
from intelligence.profiling import compute_risk_score

router = APIRouter()

@router.get("/api/offenders/{accused_id}")
def get_offender(accused_id: int, db: Session = Depends(get_db)):
    accused = db.query(Accused).filter(Accused.accused_id == accused_id).first()
    if not accused:
        raise HTTPException(status_code=404, detail="Accused not found")
        
    risk_info = compute_risk_score(
        prior_offenses=accused.prior_offense_count or 0,
        severity_avg=5, # mock
        days_since_last_crime=30, # mock
        distinct_districts=1 # mock
    )
    
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "accused": accused,
        "risk_profile": risk_info
    }

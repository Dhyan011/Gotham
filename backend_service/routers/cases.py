from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db, CaseMaster
from analytics.similarity import compute_similar_cases

router = APIRouter()

@router.get("/api/cases")
def get_cases(
    page: int = 1,
    limit: int = 20,
    crime_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CaseMaster)
    if crime_type:
        query = query.filter(CaseMaster.crime_type == crime_type)
        
    total = query.count()
    cases = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "total": total,
        "page": page,
        "cases": cases
    }

@router.get("/api/similar-cases/{fir_id}")
def get_similar_cases(fir_id: int, db: Session = Depends(get_db)):
    similar = compute_similar_cases(db, fir_id)
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "similar_cases": similar
    }

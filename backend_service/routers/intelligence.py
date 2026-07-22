from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db, Accused, CaseMaster, CaseAccused
from intelligence.entity_resolution import resolve_entities
from intelligence.behavioral import extract_crime_sequence, markov_chain_prediction, compute_escalation_slope

router = APIRouter()

class ResolveRequest(BaseModel):
    entity_a_id: int
    entity_b_id: int

@router.post("/api/intelligence/resolve")
def resolve(req: ResolveRequest, db: Session = Depends(get_db)):
    a = db.query(Accused).filter(Accused.accused_id == req.entity_a_id).first()
    b = db.query(Accused).filter(Accused.accused_id == req.entity_b_id).first()
    
    if not a or not b:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    entity_a = {"name": a.name, "descriptor": {}}
    entity_b = {"name": b.name, "descriptor": {}}
    
    result = resolve_entities(entity_a, entity_b)
    
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "fusion_result": result
    }

@router.get("/api/intelligence/behavioral/{accused_id}")
def get_behavioral(accused_id: int, db: Session = Depends(get_db)):
    cases = db.query(CaseMaster).join(CaseAccused).filter(CaseAccused.accused_id == accused_id).all()
    if not cases:
        raise HTTPException(status_code=404, detail="No cases found for accused")
        
    crimes = [{"date": c.date_of_occurrence, "crime_type": c.crime_type, "severity_weight": c.severity_weight} for c in cases if c.date_of_occurrence]
    seq = extract_crime_sequence(crimes)
    slope = compute_escalation_slope(crimes)
    
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "sequence": seq,
        "escalation_slope": slope
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import get_db, Accused, CaseAccused, CaseMaster

router = APIRouter()

@router.get("/api/network/{accused_id}")
def get_network(accused_id: int, db: Session = Depends(get_db)):
    accused = db.query(Accused).filter(Accused.accused_id == accused_id).first()
    if not accused:
        raise HTTPException(status_code=404, detail="Accused not found")
        
    # 2-hop subgraph
    # Hop 1: Cases linked to accused
    case_links = db.query(CaseAccused).filter(CaseAccused.accused_id == accused_id).all()
    fir_ids = [c.fir_id for c in case_links]
    
    # Hop 2: Other accused linked to those cases
    co_accused_links = db.query(CaseAccused).filter(CaseAccused.fir_id.in_(fir_ids)).all()
    all_accused_ids = list(set([c.accused_id for c in co_accused_links]))
    
    nodes = []
    edges = []
    
    # Add accused nodes
    accused_nodes = db.query(Accused).filter(Accused.accused_id.in_(all_accused_ids)).all()
    for a in accused_nodes:
        nodes.append({"id": f"A{a.accused_id}", "label": a.name, "type": "Accused"})
        
    # Add case nodes
    case_nodes = db.query(CaseMaster).filter(CaseMaster.fir_id.in_(fir_ids)).all()
    for c in case_nodes:
        nodes.append({"id": f"C{c.fir_id}", "label": c.fir_number, "type": "Case"})
        
    # Add edges
    for link in co_accused_links:
        edges.append({
            "source": f"A{link.accused_id}",
            "target": f"C{link.fir_id}",
            "label": link.role
        })
        
    return {
        "data_source": "GOTHAM Synthetic Dataset v1.0 \u2014 Simulated for demonstration purposes",
        "nodes": nodes,
        "edges": edges
    }

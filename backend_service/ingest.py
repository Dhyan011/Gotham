import os
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db, CaseMaster, Accused, Victim, ComplainantDetails, ArrestSurrender
from neo4j_client import neo4j_client
from sentence_transformers import SentenceTransformer

import openai

# Initialize LLM and Embedding models
print("Loading Embedding Model for Ingestion...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "mock_key")
client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

router = APIRouter()

# --- Pydantic Models for Ingestion Payload ---
class AccusedPayload(BaseModel):
    name: str
    age: Optional[int] = None
    gender_id: Optional[int] = None
    person_id: Optional[str] = None
    is_arrested: Optional[bool] = False

class VictimPayload(BaseModel):
    name: str
    age: Optional[int] = None
    gender_id: Optional[int] = None

class ComplainantPayload(BaseModel):
    name: str
    age: Optional[int] = None

class FIRPayload(BaseModel):
    crime_no: str
    case_no: Optional[str] = None
    date_registered: str
    brief_facts: str
    accused: List[AccusedPayload] = []
    victims: List[VictimPayload] = []
    complainants: List[ComplainantPayload] = []


def extract_entities_from_llm(text: str):
    """
    Uses an LLM to read the BriefFacts and extract Vehicles and BankAccounts.
    """
    if OPENROUTER_API_KEY == "mock_key":
        # Mock extraction for testing if key is missing
        if "White SUV" in text:
            return {"vehicles": ["White SUV (KA-01-AB-1234)"], "bank_accounts": []}
        return {"vehicles": [], "bank_accounts": []}

    prompt = f"""
    Analyze the following police case summary (BriefFacts). 
    Extract any Vehicles (with registration if present) and Bank Accounts mentioned.
    Return ONLY a valid JSON object in this format: {{"vehicles": ["..."], "bank_accounts": ["..."]}}
    
    BriefFacts: {text}
    """
    try:
        completion = client.chat.completions.create(
            model="google/gemini-pro",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"LLM Extraction failed: {e}")
        return {"vehicles": [], "bank_accounts": []}


@router.post("/api/ingest")
def ingest_fir(payload: FIRPayload, db: Session = Depends(get_db)):
    """
    Dynamic ingestion endpoint.
    1. Saves to Postgres.
    2. Embeds BriefFacts.
    3. Extracts Vehicles/Banks via LLM.
    4. Pushes the full intelligence subgraph to Neo4j.
    """
    # 1 & 2. Save Structured Data & Generate Embeddings
    try:
        embedding = embedder.encode(payload.brief_facts).tolist()
        
        # Check if Case exists
        db_case = db.query(CaseMaster).filter(CaseMaster.CrimeNo == payload.crime_no).first()
        if not db_case:
            db_case = CaseMaster(
                CrimeNo=payload.crime_no,
                CaseNo=payload.case_no,
                CrimeRegisteredDate=datetime.strptime(payload.date_registered, "%Y-%m-%d").date(),
                BriefFacts=payload.brief_facts,
                embedding=embedding
            )
            db.add(db_case)
            db.commit()
            db.refresh(db_case)
        
        # Process Accused
        for acc in payload.accused:
            db_acc = Accused(
                CaseMasterID=db_case.CaseMasterID,
                AccusedName=acc.name,
                AgeYear=acc.age,
                GenderID=acc.gender_id,
                PersonID=acc.person_id
            )
            db.add(db_acc)
            if acc.is_arrested:
                db.flush() # get ID
                db_arrest = ArrestSurrender(
                    CaseMasterID=db_case.CaseMasterID,
                    AccusedMasterID=db_acc.AccusedMasterID,
                    IsAccused=True
                )
                db.add(db_arrest)

        # Process Victims
        for vic in payload.victims:
            db_vic = Victim(
                CaseMasterID=db_case.CaseMasterID,
                VictimName=vic.name,
                AgeYear=vic.age,
                GenderID=vic.gender_id
            )
            db.add(db_vic)

        # Process Complainants
        for comp in payload.complainants:
            db_comp = ComplainantDetails(
                CaseMasterID=db_case.CaseMasterID,
                ComplainantName=comp.name,
                AgeYear=comp.age
            )
            db.add(db_comp)
            
        db.commit()

        # 3. LLM Entity Extraction
        extracted = extract_entities_from_llm(payload.brief_facts)
        
        # 4. Push everything to Neo4j
        cypher_queries = [
            # Ensure FIR node exists
            f"MERGE (f:FIR {{crime_no: '{payload.crime_no}'}})"
        ]
        
        for acc in payload.accused:
            # Note: Using MERGE for Person to ensure we link repeat offenders across FIRs
            cypher_queries.append(f"MERGE (p:Person {{name: '{acc.name}'}})")
            cypher_queries.append(f"MATCH (p:Person {{name: '{acc.name}'}}), (f:FIR {{crime_no: '{payload.crime_no}'}}) MERGE (p)-[:ACCUSED_IN]->(f)")
        
        for vic in payload.victims:
            cypher_queries.append(f"MERGE (p:Person {{name: '{vic.name}'}})")
            cypher_queries.append(f"MATCH (p:Person {{name: '{vic.name}'}}), (f:FIR {{crime_no: '{payload.crime_no}'}}) MERGE (p)-[:VICTIM_IN]->(f)")
            
        for veh in extracted.get("vehicles", []):
            cypher_queries.append(f"MERGE (v:Vehicle {{name: '{veh}'}})")
            cypher_queries.append(f"MATCH (v:Vehicle {{name: '{veh}'}}), (f:FIR {{crime_no: '{payload.crime_no}'}}) MERGE (v)-[:USED_IN]->(f)")

        # Execute Graph insertion
        with neo4j_client.driver.session() as session:
            for q in cypher_queries:
                session.run(q)

        return {
            "status": "success", 
            "message": f"FIR {payload.crime_no} ingested.",
            "postgres_id": db_case.CaseMasterID,
            "ai_extracted_entities": extracted
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

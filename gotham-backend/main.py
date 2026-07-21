from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our hackathon modules
from neo4j_client import neo4j_client
from ml_engine import calculate_risk_score, semantic_search
from copilot import run_investigation_pipeline, generate_ai_summary

app = FastAPI(title="GOTHAM Intelligence Engine (Hackathon Edition)")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Models ---
class CopilotRequest(BaseModel):
    command: str

class SemanticSearchRequest(BaseModel):
    query: str

# --- 5 Core Endpoints ---

@app.get("/api/cases/{case_id}")
def get_case(case_id: int):
    """Returns the core Case Management object."""
    if case_id != 1:
        raise HTTPException(status_code=404, detail="Case not found. (Use Case 1 for Demo)")
    
    return {
        "id": 1,
        "title": "Operation MG Road Syndicate",
        "status": "OPEN",
        "assigned_officer": "Inspector Raj",
        "primary_fir": "FIR-1245",
        "ai_summary": generate_ai_summary(),
        "timeline_events": [
            {"date": "2025-06-15", "event": "Vehicle KA-01-AB-1234 registered to Ravi Kumar."},
            {"date": "2025-07-06", "event": "FIR-1246 (Extortion) registered in Indiranagar."},
            {"date": "2025-07-19", "event": "FIR-1245 (Armed Robbery) registered on MG Road."}
        ]
    }

@app.get("/api/graph/neighbors")
def get_graph_neighbors(person_name: str = "Ravi Kumar"):
    """Returns the Neo4j ontology graph for the UI."""
    return neo4j_client.get_person_neighbors(person_name)

@app.get("/api/risk/score")
def get_risk_score(person_name: str):
    """Returns the XGBoost risk score and confidence reasoning."""
    return calculate_risk_score(person_name)

@app.post("/api/search/semantic")
def search_semantic(req: SemanticSearchRequest):
    """Returns pgvector semantic search matches."""
    return semantic_search(req.query)

@app.post("/api/copilot/investigate")
def copilot_investigate(req: CopilotRequest):
    """
    The Golden Demo Endpoint.
    Triggers the sequential pipeline animation for the given FIR.
    """
    if "1245" not in req.command:
        raise HTTPException(status_code=400, detail="Demo restricted to FIR-1245.")
    
    pipeline_steps = run_investigation_pipeline("FIR-1245")
    return {"status": "success", "pipeline": pipeline_steps}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

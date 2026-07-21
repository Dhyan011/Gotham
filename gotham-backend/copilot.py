"""
Investigation Copilot Orchestrator
Provides the "Golden Demo" pipeline for 'Investigate FIR 1245'
"""

def run_investigation_pipeline(fir_no: str):
    """
    Simulates the 10-step AI Orchestrator pipeline.
    Returns a sequenced list of events for the UI to animate.
    """
    return [
        {
            "step": 1,
            "action": "Graph Traversal",
            "message": "Traversing Neo4j Ontology for FIR-1245...",
            "result": "Found 3 connected suspects and 1 Vehicle (White SUV: KA-01-AB-1234)."
        },
        {
            "step": 2,
            "action": "Community Detection (Louvain)",
            "message": "Running Louvain algorithm on subgraph...",
            "result": "Identified 'White SUV Syndicate' (Confidence: 94% - Dense co-accused linkage)."
        },
        {
            "step": 3,
            "action": "XGBoost Risk Scoring",
            "message": "Calculating risk scores for connected individuals...",
            "result": "Ravi Kumar flagged as High Risk (85.0) - High Betweenness Centrality."
        },
        {
            "step": 4,
            "action": "Semantic Search (pgvector)",
            "message": "Searching for similar historical cases...",
            "result": "Found FIR-1246 (Extortion) matching vehicle description (Similarity: 92%)."
        },
        {
            "step": 5,
            "action": "Next Best Action",
            "message": "Generating recommendations...",
            "result": "RECOMMENDATION: Interview Suresh M regarding his association with Ravi Kumar and vehicle KA-01-AB-1234."
        }
    ]

def generate_ai_summary():
    """Single direct LLM call mock for the case view."""
    return (
        "Investigation into FIR-1245 reveals a highly organized network. "
        "The suspects (Suresh M, Kiran Patel) utilized a White SUV owned by Ravi Kumar, "
        "who acts as a central broker. Semantic search connects this group to a prior extortion case (FIR-1246). "
        "It is highly probable this is a coordinated syndicate."
    )

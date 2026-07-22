"""
ML Engine: XGBoost Risk Scorer & Semantic Search (pgvector)
"""

def calculate_risk_score(person_id: str):
    """
    Mock XGBoost Risk Scorer for the Hackathon Demo.
    Returns a score out of 100 with an explainable evidence trail.
    """
    # For Ravi Kumar (Leader)
    if person_id == "Ravi Kumar":
        return {
            "score": 85.0,
            "confidence": "89%",
            "reasoning": "89% - High Betweenness Centrality + Owner of flagged vehicle."
        }
    # For Suresh M
    elif person_id == "Suresh M":
        return {
            "score": 72.0,
            "confidence": "81%",
            "reasoning": "81% - Direct co-accused link to high-risk individual."
        }
    return {
        "score": 12.0,
        "confidence": "99%",
        "reasoning": "99% - No prior history, likely victim or bystander."
    }

def semantic_search(query: str):
    """
    Mock pgvector semantic search.
    Query: "White SUV robbery near MG Road"
    """
    # In a real app, we use sentence-transformers to embed `query` 
    # and run `<->` operator in Postgres (pgvector) against FIR.embedding.
    return {
        "top_match": "FIR-1245",
        "similarity": "0.92",
        "confidence": "92%",
        "reasoning": "92% - High semantic overlap with 'Armed Robbery' and 'White SUV'."
    }

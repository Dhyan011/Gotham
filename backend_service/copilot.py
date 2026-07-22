import os
import openai
from osint_engine import gather_osint_for_entity

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "mock_key")
client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

def run_investigation_pipeline(fir_no: str):
    """
    Simulates the AI Orchestrator pipeline, now featuring OSINT.
    Returns a sequenced list of events for the UI to animate.
    """
    return [
        {
            "step": 1,
            "action": "Graph Traversal",
            "message": f"Traversing Neo4j Ontology for {fir_no}...",
            "result": "Found 3 connected suspects and 1 Vehicle (White SUV: KA-01-AB-1234)."
        },
        {
            "step": 2,
            "action": "Open Source Intelligence (OSINT)",
            "message": "Scraping live internet for digital footprint...",
            "result": "Discovered 3 recent news articles matching suspects."
        },
        {
            "step": 3,
            "action": "Community Detection (Louvain)",
            "message": "Running Louvain algorithm on subgraph...",
            "result": "Identified 'White SUV Syndicate' (Confidence: 94% - Dense co-accused linkage)."
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

def generate_ai_summary(suspect_name: str = "Ravi Kumar"):
    """
    Live LLM call via OpenRouter incorporating live OSINT data.
    """
    osint_context = gather_osint_for_entity(suspect_name)
    
    if OPENROUTER_API_KEY == "mock_key":
        return (
            f"Investigation reveals a highly organized network led by {suspect_name}. "
            "The suspects utilized a White SUV owned by the leader. "
            f"LIVE OSINT MATCH: {osint_context}"
        )

    prompt = f"""
    You are an AI Police Intelligence Analyst. Provide a brief, 3-sentence intelligence summary 
    about a suspect named '{suspect_name}'. Incorporate the following live internet OSINT data into your summary:
    
    {osint_context}
    """
    try:
        completion = client.chat.completions.create(
            model="google/gemini-pro",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"LLM Summary Failed: {e}")
        return "Failed to generate AI summary. Ensure OpenRouter API key is set."

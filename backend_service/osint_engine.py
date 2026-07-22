"""
OSINT Engine: Automated Digital Footprinting via DuckDuckGo
"""
from duckduckgo_search import DDGS
from typing import List, Dict

def perform_web_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Searches the live web for the given query (e.g., suspect name or gang).
    Returns a list of dictionaries with 'title', 'href', and 'body'.
    """
    results = []
    try:
        with DDGS() as ddgs:
            # text() generates results; we take the first max_results
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        print(f"OSINT Web Search Failed: {e}")
    
    return results

def gather_osint_for_entity(entity_name: str) -> str:
    """
    Gathers OSINT for a specific entity and formats it into a summary string
    that can be fed to the LLM during the Copilot pipeline.
    """
    print(f"Gathering OSINT for: {entity_name}")
    
    # We append keywords to narrow the search to crime/news
    query = f'"{entity_name}" AND (arrest OR police OR crime OR gang)'
    
    results = perform_web_search(query, max_results=3)
    
    if not results:
        return f"No significant OSINT findings for '{entity_name}'."
        
    osint_summary = f"OSINT Intelligence for '{entity_name}':\n"
    for idx, r in enumerate(results, 1):
        osint_summary += f"{idx}. {r['title']} ({r['url']})\n   {r['snippet']}\n"
        
    return osint_summary

# Test execution
if __name__ == "__main__":
    # Example search
    print(gather_osint_for_entity("Ravi Kumar"))

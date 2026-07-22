"""
GOTHAM Graph Algorithms
Implements PageRank, Betweenness Centrality, Louvain Community Detection,
and Link Prediction for criminal network intelligence.
"""
import networkx as nx
from collections import defaultdict
import math


def compute_pagerank(G, alpha=0.85):
    """
    Weighted PageRank to find the most INFLUENTIAL nodes in the criminal network.
    
    Criminology insight: High PageRank does NOT mean most arrested.
    It means the person who is most connected through important intermediaries.
    This often identifies the ORGANIZER who appears in fewer cases but whose
    associates are involved in many.
    """
    try:
        pr = nx.pagerank(G, alpha=alpha, weight='weight')
    except Exception:
        pr = {n: 1.0 / G.number_of_nodes() for n in G.nodes()}
    
    # Filter to accused nodes only and rank
    accused_pr = {node: score for node, score in pr.items()
                  if G.nodes[node].get("type") == "Accused"}
    ranked = sorted(accused_pr.items(), key=lambda x: x[1], reverse=True)
    return ranked


def compute_betweenness(G):
    """
    Betweenness Centrality to find BROKERS in the network.
    
    Criminology insight: High betweenness = the person who bridges
    otherwise disconnected criminal groups. Removing this node
    fragments the network — making them a high-priority target.
    """
    try:
        bc = nx.betweenness_centrality(G, weight='weight', normalized=True)
    except Exception:
        bc = {n: 0.0 for n in G.nodes()}
    
    accused_bc = {node: score for node, score in bc.items()
                  if G.nodes[node].get("type") == "Accused"}
    ranked = sorted(accused_bc.items(), key=lambda x: x[1], reverse=True)
    return ranked


def detect_communities(G):
    """
    Louvain community detection to automatically discover GANG CLUSTERS.
    
    Criminology insight: Communities in the co-accused graph represent
    groups of people who frequently offend together — potential organized
    crime units. No manual tagging needed.
    """
    try:
        import community as community_louvain
        G_undirected = G.to_undirected()
        partition = community_louvain.best_partition(G_undirected, weight='weight')
    except ImportError:
        # Fallback: simple connected components as communities
        G_undirected = G.to_undirected()
        partition = {}
        for i, component in enumerate(nx.connected_components(G_undirected)):
            for node in component:
                partition[node] = i
    
    # Build community summaries
    communities = defaultdict(list)
    for node, comm_id in partition.items():
        if G.nodes[node].get("type") == "Accused":
            communities[comm_id].append(node)
    
    # Filter to communities with 2+ accused members
    result = {}
    for comm_id, members in communities.items():
        if len(members) >= 2:
            result[comm_id] = {
                "community_id": comm_id,
                "members": members,
                "size": len(members),
                "member_names": [G.nodes[m].get("label", m) for m in members]
            }
    
    return partition, result


def predict_links(G, threshold_jaccard=0.3, threshold_aa=1.5):
    """
    Link Prediction using Jaccard coefficient + Adamic-Adar index.
    
    Criminology insight: Two accused who share many co-accused but
    are NOT directly linked may have an undiscovered connection.
    These "predicted links" surface probable associations for investigation.
    """
    accused_nodes = [n for n in G.nodes() if G.nodes[n].get("type") == "Accused"]
    G_undirected = G.to_undirected()
    
    predicted_links = []
    
    # Only check pairs that are NOT directly connected
    for i in range(len(accused_nodes)):
        for j in range(i + 1, len(accused_nodes)):
            u, v = accused_nodes[i], accused_nodes[j]
            if G_undirected.has_edge(u, v):
                continue
            
            neighbors_u = set(G_undirected.neighbors(u))
            neighbors_v = set(G_undirected.neighbors(v))
            common = neighbors_u & neighbors_v
            
            if not common:
                continue
            
            union = neighbors_u | neighbors_v
            jaccard = len(common) / len(union) if union else 0
            
            # Adamic-Adar: weighted by inverse log of neighbor degree
            adamic_adar = 0
            for w in common:
                deg = G_undirected.degree(w)
                if deg > 1:
                    adamic_adar += 1.0 / math.log(deg)
            
            if jaccard > threshold_jaccard or adamic_adar > threshold_aa:
                reasons = []
                if jaccard > threshold_jaccard:
                    reasons.append(f"Jaccard coefficient: {jaccard:.3f}")
                if adamic_adar > threshold_aa:
                    reasons.append(f"Adamic-Adar index: {adamic_adar:.3f}")
                reasons.append(f"{len(common)} common associates")
                
                predicted_links.append({
                    "entity_a": u,
                    "entity_b": v,
                    "entity_a_name": G.nodes[u].get("label", u),
                    "entity_b_name": G.nodes[v].get("label", v),
                    "jaccard": round(jaccard, 4),
                    "adamic_adar": round(adamic_adar, 4),
                    "confidence": round(min(1.0, (jaccard + adamic_adar / 3) / 1.3), 3),
                    "inference_reason": reasons
                })
    
    predicted_links.sort(key=lambda x: x["confidence"], reverse=True)
    return predicted_links


if __name__ == "__main__":
    from builder import build_crime_graph
    G = build_crime_graph()
    
    print("═" * 60)
    print("GOTHAM Graph Analytics Report")
    print("═" * 60)
    
    pr = compute_pagerank(G)
    print("\n🔴 Top 10 Most Influential (PageRank):")
    for node, score in pr[:10]:
        print(f"  {G.nodes[node]['label']:25s} → {score:.6f}")
    
    bc = compute_betweenness(G)
    print("\n🔵 Top 10 Network Brokers (Betweenness):")
    for node, score in bc[:10]:
        print(f"  {G.nodes[node]['label']:25s} → {score:.6f}")
    
    partition, communities = detect_communities(G)
    print(f"\n🟢 Detected {len(communities)} communities (gangs):")
    for cid, info in list(communities.items())[:5]:
        print(f"  Community {cid}: {info['size']} members — {', '.join(info['member_names'][:4])}")
    
    links = predict_links(G)
    print(f"\n🟡 Predicted Links (probable hidden connections): {len(links)}")
    for link in links[:5]:
        print(f"  {link['entity_a_name']} ↔ {link['entity_b_name']} (confidence: {link['confidence']})")

"""
GOTHAM Graph Builder
Constructs a NetworkX MultiDiGraph from the PostgreSQL database.
Nodes: Accused, Victim, CaseMaster, Unit, LocationEntity
Edges: INVOLVED_IN, CO_ACCUSED, VICTIMIZED_IN, OCCURRED_AT, OPERATES_AT
"""
import networkx as nx
from collections import defaultdict
from database import SessionLocal, CaseMaster, Accused, CaseAccused, Victim, Unit


def build_crime_graph():
    """
    Build the full GOTHAM crime intelligence graph from database records.
    
    Graph structure mirrors real criminal network analysis:
    - Accused nodes are the primary investigation targets
    - Case nodes represent FIRs (the events connecting entities)
    - Co-accused edges reveal criminal partnerships
    - Shared locations/times reveal operational patterns
    """
    G = nx.MultiDiGraph()
    db = SessionLocal()

    try:
        # ── Add Accused nodes ──
        for acc in db.query(Accused).all():
            G.add_node(f"accused_{acc.accused_id}", 
                       type="Accused", label=acc.name,
                       id=acc.accused_id,
                       risk_score=float(acc.risk_score or 0),
                       risk_label=acc.risk_label or "LOW",
                       district=acc.district,
                       prior_offenses=acc.prior_offense_count or 0,
                       mo_pattern=acc.mo_pattern or [])

        # ── Add Case nodes ──
        for case in db.query(CaseMaster).all():
            G.add_node(f"case_{case.fir_id}",
                       type="Case", label=case.fir_number,
                       id=case.fir_id,
                       crime_type=case.crime_type,
                       severity=case.severity_weight or 1,
                       date=str(case.date_of_occurrence),
                       district=None,
                       lat=float(case.lat or 0), lng=float(case.lng or 0))

        # ── Add Unit (station) nodes ──
        for unit in db.query(Unit).all():
            G.add_node(f"unit_{unit.unit_id}",
                       type="Unit", label=unit.unit_name,
                       id=unit.unit_id,
                       district=unit.district,
                       lat=float(unit.lat or 0), lng=float(unit.lng or 0))

        # ── Add Victim nodes ──
        for victim in db.query(Victim).all():
            G.add_node(f"victim_{victim.victim_id}",
                       type="Victim", label=victim.name,
                       id=victim.victim_id)

        # ── Add INVOLVED_IN edges (accused → case) ──
        co_accused_map = defaultdict(list)  # fir_id → [accused_ids]
        for link in db.query(CaseAccused).all():
            case_node = f"case_{link.fir_id}"
            accused_node = f"accused_{link.accused_id}"
            if G.has_node(case_node) and G.has_node(accused_node):
                severity = G.nodes[case_node].get("severity", 1)
                G.add_edge(accused_node, case_node,
                           relationship="INVOLVED_IN",
                           role=link.role,
                           weight=severity)
                co_accused_map[link.fir_id].append(link.accused_id)

        # ── Add CO_ACCUSED edges (accused ↔ accused via shared cases) ──
        # Criminology: co-accused relationships are the backbone of network analysis.
        # Frequency of co-occurrence is a strong indicator of organized crime membership.
        co_accused_weight = defaultdict(int)
        for fir_id, acc_ids in co_accused_map.items():
            for i in range(len(acc_ids)):
                for j in range(i + 1, len(acc_ids)):
                    pair = tuple(sorted([acc_ids[i], acc_ids[j]]))
                    co_accused_weight[pair] += 1

        for (a1, a2), weight in co_accused_weight.items():
            G.add_edge(f"accused_{a1}", f"accused_{a2}",
                       relationship="CO_ACCUSED", weight=weight)
            G.add_edge(f"accused_{a2}", f"accused_{a1}",
                       relationship="CO_ACCUSED", weight=weight)

        # ── Add VICTIMIZED_IN edges (victim → case) ──
        for victim in db.query(Victim).all():
            victim_node = f"victim_{victim.victim_id}"
            case_node = f"case_{victim.fir_id}"
            if G.has_node(victim_node) and G.has_node(case_node):
                G.add_edge(victim_node, case_node, relationship="VICTIMIZED_IN", weight=1)

        # ── Add OCCURRED_AT edges (case → unit) ──
        for case in db.query(CaseMaster).all():
            if case.unit_id:
                G.add_edge(f"case_{case.fir_id}", f"unit_{case.unit_id}",
                           relationship="OCCURRED_AT", weight=1)

    finally:
        db.close()

    print(f"📊 Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def get_subgraph(G, center_node, hops=2):
    """
    Extract a subgraph around a center node up to N hops.
    Used for network visualization of an individual accused's connections.
    """
    if center_node not in G:
        return {"nodes": [], "edges": []}

    # BFS to find all nodes within N hops
    visited = {center_node}
    frontier = {center_node}
    for _ in range(hops):
        next_frontier = set()
        for node in frontier:
            for neighbor in set(G.successors(node)) | set(G.predecessors(node)):
                if neighbor not in visited:
                    next_frontier.add(neighbor)
                    visited.add(neighbor)
        frontier = next_frontier

    subgraph = G.subgraph(visited)
    
    nodes = []
    for node_id in subgraph.nodes():
        data = dict(subgraph.nodes[node_id])
        data["node_id"] = node_id
        nodes.append(data)

    edges = []
    for u, v, data in subgraph.edges(data=True):
        edges.append({
            "source": u, "target": v,
            "relationship": data.get("relationship", "UNKNOWN"),
            "weight": data.get("weight", 1)
        })

    return {"nodes": nodes, "edges": edges}


# Singleton graph instance
_graph_instance = None

def get_graph():
    """Get or build the singleton graph instance."""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = build_crime_graph()
    return _graph_instance

def rebuild_graph():
    """Force rebuild the graph from current DB state."""
    global _graph_instance
    _graph_instance = build_crime_graph()
    return _graph_instance


if __name__ == "__main__":
    G = build_crime_graph()
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    # Show top 5 accused by degree
    accused_nodes = [n for n in G.nodes() if G.nodes[n].get("type") == "Accused"]
    degrees = [(n, G.degree(n)) for n in accused_nodes]
    degrees.sort(key=lambda x: x[1], reverse=True)
    print("\nTop 5 accused by connections:")
    for node, deg in degrees[:5]:
        print(f"  {G.nodes[node]['label']}: {deg} connections")

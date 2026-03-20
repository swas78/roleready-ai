import json
import os
import networkx as nx

def load_graph():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "skill_graph.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def topological_sort(skills_to_learn: list[str]) -> list[str]:
    # Builds NetworkX DiGraph with only relevant skills
    graph_data = load_graph()
    
    G = nx.DiGraph()
    
    # We want prereq -> skill directed edges
    lower_map = {s.lower(): s for s in skills_to_learn}
    
    # Add nodes
    for skill in skills_to_learn:
        G.add_node(skill)
        
    # Attempt to add edges if prereq is also in skills_to_learn
    for skill_name, data in graph_data.items():
        if skill_name.lower() in lower_map:
            actual_skill_name = lower_map[skill_name.lower()]
            prereqs = data.get("prereqs", [])
            for pr in prereqs:
                if pr.lower() in lower_map:
                    actual_prereq_name = lower_map[pr.lower()]
                    G.add_edge(actual_prereq_name, actual_skill_name)
                    
    # Break cycles defensively
    while not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        if not cycles: break
        # remove arbitrary edge in cycle to break it
        cyc = cycles[0]
        G.remove_edge(cyc[0], cyc[1])
        
    ordered = list(nx.topological_sort(G))
    return ordered

def get_prereq_chain(skill: str) -> list[str]:
    graph_data = load_graph()
    visited = set()
    chain = []
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for s, d in graph_data.items():
            if s.lower() == node.lower():
                for pr in d.get("prereqs", []):
                    dfs(pr)
                    if pr not in chain:
                        chain.append(pr)
    
    dfs(skill)
    return chain

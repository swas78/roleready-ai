import json
import os
from api.schemas import RoadmapModule, GapObject
from core.embedder import Embedder

def load_catalog():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "catalog.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_to_catalog(skill: str, domain: str, embedder: Embedder):
    catalog = load_catalog()
    # Filter by domain
    filtered = [c for c in catalog if c.get("domain") in (domain, "both")]
    if not filtered:
        return None
        
    candidate_strings = []
    for c in filtered:
        skills_str = ", ".join(c.get("skills_covered", []))
        candidate_strings.append(f"{c['title']} {skills_str}")
        
    best_str, score = embedder.best_match(skill, candidate_strings)
    
    if score < 0.45:
        return None
        
    best_idx = candidate_strings.index(best_str)
    return filtered[best_idx]

def build_roadmap(ordered_skills: list[str], embedder: Embedder, domain: str, gap_object: GapObject) -> list[RoadmapModule]:
    roadmap_modules = []
    seen_module_ids = set()
    
    partial_skill_names = set(s.name.lower() for s in gap_object.partial)
    
    order_idx = 1
    for skill in ordered_skills:
        match = match_to_catalog(skill, domain, embedder)
        if match:
            mod_id = match["id"]
            if mod_id not in seen_module_ids:
                seen_module_ids.add(mod_id)
                # Determine type
                mod_type = "refresher" if skill.lower() in partial_skill_names else "new"
                
                rm = RoadmapModule(
                    module_id=mod_id,
                    title=match["title"],
                    duration_hours=match.get("duration_hours", 10),
                    type=mod_type,
                    order=order_idx,
                    reason="", # Left empty for tracer to fill
                    skills_covered=match.get("skills_covered", []),
                    domain=match.get("domain", "tech"),
                    level=match.get("level", "intermediate")
                )
                roadmap_modules.append(rm)
                order_idx += 1
                
    return roadmap_modules

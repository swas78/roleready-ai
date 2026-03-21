import json
import os
import asyncio
import logging
from groq import AsyncGroq
from api.schemas import RoadmapModule, GapObject
from core.embedder import Embedder

logger = logging.getLogger(__name__)

# Try to initialize Groq client for dynamic modules
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", "your_key"))
MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

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

async def generate_dynamic_module(skill: str, domain: str, mod_type: str, order_idx: int) -> RoadmapModule:
    prompt = f"""
    Create a highly realistic and specific learning module for a professional trying to learn or refresh the skill: "{skill}" in the domain: "{domain}".
    Return ONLY a valid JSON object with the following keys. No markdown or explanation.
    - "title": string (catchy course title)
    - "duration_hours": integer (between 2 and 20)
    - "skills_covered": array of strings (3 to 6 related sub-skills)
    - "level": string ("beginner", "intermediate", "advanced")
    - "difficulty": string ("easy", "medium", "hard")
    """
    
    try:
        completion = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = completion.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        data = json.loads(content)
        
        return RoadmapModule(
            module_id=f"dyn_{skill.lower().replace(' ', '_')}",
            title=data.get("title", f"Mastering {skill}"),
            duration_hours=data.get("duration_hours", 5),
            type=mod_type,
            order=order_idx,
            reason="",
            skills_covered=data.get("skills_covered", [skill]),
            domain=domain,
            level=data.get("level", "intermediate"),
            difficulty=data.get("difficulty", "medium")
        )
    except Exception as e:
        logger.error(f"Failed to generate dynamic module for {skill}: {e}")
        # Fallback
        return RoadmapModule(
            module_id=f"fb_{skill.lower().replace(' ', '_')}",
            title=f"Fundamentals of {skill}",
            duration_hours=4,
            type=mod_type,
            order=order_idx,
            reason="",
            skills_covered=[skill],
            domain=domain,
            level="intermediate",
            difficulty="medium"
        )

async def build_roadmap(ordered_skills: list[str], embedder: Embedder, domain: str, gap_object: GapObject) -> list[RoadmapModule]:
    roadmap_modules = []
    seen_module_ids = set()
    
    partial_skill_names = set(s.name.lower() for s in gap_object.partial)
    
    order_idx = 1
    
    # Process each skill
    for skill in ordered_skills:
        mod_type = "refresher" if skill.lower() in partial_skill_names else "new"
        match = match_to_catalog(skill, domain, embedder)
        
        if match:
            mod_id = match["id"]
            if mod_id not in seen_module_ids:
                seen_module_ids.add(mod_id)
                rm = RoadmapModule(
                    module_id=mod_id,
                    title=match["title"],
                    duration_hours=match.get("duration_hours", 10),
                    type=mod_type,
                    order=order_idx,
                    reason="", 
                    skills_covered=match.get("skills_covered", []),
                    domain=match.get("domain", "tech"),
                    level=match.get("level", "intermediate"),
                    difficulty=match.get("difficulty", "medium")
                )
                roadmap_modules.append(rm)
                order_idx += 1
        else:
            # Generate dynamically if not found in static catalog
            rm = await generate_dynamic_module(skill, domain, mod_type, order_idx)
            if rm.module_id not in seen_module_ids:
                seen_module_ids.add(rm.module_id)
                roadmap_modules.append(rm)
                order_idx += 1
                
    return roadmap_modules

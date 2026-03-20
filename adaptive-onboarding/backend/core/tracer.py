from api.schemas import RoadmapModule, GapObject, ExtractedSkill
from core.graph import get_prereq_chain

def attach_reasons(roadmap: list[RoadmapModule], gap: GapObject, candidate_skills: list[ExtractedSkill], required_skills: list[str]) -> list[RoadmapModule]:
    # Extract lower sets for easy matching
    missing_lower = set(s.lower() for s in gap.missing)
    partial_map = {s.name.lower(): s for s in gap.partial}
    
    for mod in roadmap:
        reasons = []
        covered_missing = [s for s in mod.skills_covered if s.lower() in missing_lower]
        covered_partial = [s for s in mod.skills_covered if s.lower() in partial_map]
        
        # Missing reasons
        if covered_missing:
            skills_str = ", ".join(covered_missing)
            reasons.append(f"The Job Description explicitly requires {skills_str}, which were not detected in your resume.")
            
        # Partial reasons
        for ps in covered_partial:
            skill_obj = partial_map[ps.lower()]
            if skill_obj.confidence < 50:
                reasons.append(f"You mentioned {ps} briefly, but lacked sufficient project context to confirm deep expertise.")
            else:
                reasons.append(f"You have some experience with {ps}, but an advanced refresher is recommended to meet JD parity.")
                
        # Optional Prerequisite Chaining
        for s in covered_missing + covered_partial:
            chain = get_prereq_chain(s)
            if chain:
                reasons.append(f"Note: Mastery of {s} relies on understanding {', '.join(chain)}.")
                
        mod.reason = " ".join(reasons)
        if not mod.reason:
            mod.reason = "Recommended bridging module based on implicit semantic skill gaps."
            
    return roadmap

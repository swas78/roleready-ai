import os
import math
from api.schemas import GapObject, ExtractedSkill
from core.embedder import Embedder

HIGH_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.75"))
LOW_THRESHOLD = float(os.getenv("PARTIAL_THRESHOLD", "0.42"))

def classify_gaps(candidate_skills: list[ExtractedSkill], required_skills: list[str], embedder: Embedder) -> GapObject:
    if not required_skills:
        return GapObject(known=candidate_skills, partial=[], missing=[])
    if not candidate_skills:
        return GapObject(known=[], partial=[], missing=required_skills)
        
    cand_strings = [s.name for s in candidate_skills]
    
    # We want matrix of shape (len(required), len(cand))
    matrix = embedder.similarity_matrix(required_skills, cand_strings)
    
    known = []
    partial = []
    missing = []
    
    matched_cand_indices = set()
    
    for i, req in enumerate(required_skills):
        best_cand_idx = -1
        best_score = -1.0
        
        for j, score in enumerate(matrix[i]):
            if score > best_score:
                best_score = score
                best_cand_idx = j
                
        if best_score >= HIGH_THRESHOLD:
            cand_skill = candidate_skills[best_cand_idx]
            if cand_skill.confidence >= 55:
                # Fully known
                known.append(cand_skill)
                matched_cand_indices.add(best_cand_idx)
            else:
                # High semantic match but low confidence (e.g. read an article) => partial
                partial.append(cand_skill)
                matched_cand_indices.add(best_cand_idx)
                
        elif best_score >= LOW_THRESHOLD:
            # Semantic match is okay but weak => partial
            cand_skill = candidate_skills[best_cand_idx]
            partial.append(cand_skill)
            matched_cand_indices.add(best_cand_idx)
            
        else:
            missing.append(req)
            
    # Include un-matched candidate skills to known arbitrarily? The spec only asks for analyzing required skills.
    # The gap object 'known' represents which required skills are known, plus extra skills candidate has.
    for j, cand in enumerate(candidate_skills):
        if j not in matched_cand_indices:
            known.append(cand)
            
    return GapObject(known=known, partial=partial, missing=missing)

def compute_readiness(gap_object: GapObject) -> int:
    # (known*1.0 + partial*0.5) / total * 100
    known_count = len(gap_object.known)
    partial_count = len(gap_object.partial)
    missing_count = len(gap_object.missing)
    
    total = known_count + partial_count + missing_count
    if total == 0:
        return 100
        
    score = ((known_count * 1.0) + (partial_count * 0.5)) / total * 100
    return int(math.clamp(score, 0, 100) if hasattr(math, 'clamp') else max(0, min(100, score)))

def get_skill_detail():
    pass # Per the spec: per-skill table data for /results/skills page. Not fully defined schemas, returning empty for now.

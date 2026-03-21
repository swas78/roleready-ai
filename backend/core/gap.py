import os
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

    required_known = []        # Required skills that candidate has (either known or partial)
    extra_skills = []          # Skills candidate has that aren't required
    missing = []               # Required skills candidate doesn't have

    matched_cand_indices = set()

    for i, req in enumerate(required_skills):
        best_cand_idx = -1
        best_score = -1.0

        for j, score in enumerate(matrix[i]):
            if score > best_score:
                best_score = score
                best_cand_idx = j

        if best_score >= HIGH_THRESHOLD:
            # High semantic match - this is a known required skill
            cand_skill = candidate_skills[best_cand_idx]
            required_known.append(cand_skill)
            matched_cand_indices.add(best_cand_idx)

        elif best_score >= LOW_THRESHOLD:
            # Moderate semantic match - partially matches required skill
            cand_skill = candidate_skills[best_cand_idx]
            required_known.append(cand_skill)  # Still counts as addressing the required skill
            matched_cand_indices.add(best_cand_idx)

        else:
            # No good match - skill is missing
            missing.append(req)

    # Extra skills: candidate has them but they weren't required
    for j, cand in enumerate(candidate_skills):
        if j not in matched_cand_indices:
            extra_skills.append(cand)

    # 'known' = required skills the candidate has (high + moderate matches)
    # Separate out actual partial matches by confidence level
    partial = []
    truly_known = []
    for skill in required_known:
        if skill.confidence < 55:
            partial.append(skill)
        else:
            truly_known.append(skill)

    return GapObject(known=truly_known, partial=partial, missing=missing)

def compute_readiness(gap_object: GapObject) -> int:
    """
    Compute readiness score based on required skills coverage.
    Formula: (fully_known_count + 0.5 * partial_count) / total_required * 100

    This correctly reflects that missing required skills should heavily reduce readiness.
    A candidate with 1 known + 9 missing = 10% readiness (not useful)
    A candidate with 5 known + 5 missing = 50% readiness (moderate)
    """
    known_count = len(gap_object.known)
    partial_count = len(gap_object.partial)
    missing_count = len(gap_object.missing)

    total = known_count + partial_count + missing_count
    if total == 0:
        return 100

    # Correct formula: known skills + partial contribution vs total required
    score = ((known_count * 1.0) + (partial_count * 0.5)) / total * 100
    return int(max(0, min(100, score)))

def get_skill_detail():
    pass # Per the spec: per-skill table data for /results/skills page. Not fully defined schemas, returning empty for now.

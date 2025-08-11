# app/inference_engine.py
from typing import Dict, Any, List
from .knowledge_base import CHICKEN_FRAMES, RECIPE_FRAMES, RULES

def age_in_range(age_weeks: int, rng: tuple) -> bool:
    return rng[0] <= age_weeks <= rng[1]

def apply_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return list of rule 'then' outputs where 'if' matches facts."""
    results = []
    for rule in RULES:
        conds = rule.get("if", {})
        match = True
        for k, v in conds.items():
            if k not in facts:
                match = False
                break
            fv = facts[k]
            if isinstance(v, tuple):
                if not (v[0] <= fv <= v[1]):
                    match = False
                    break
            else:
                if fv != v:
                    match = False
                    break
        if match:
            results.append(rule.get("then"))
    return results

def recommend_feed(chicken_type: str, age_weeks: int, include_recipes: bool=True):
    facts = {"Type": chicken_type.capitalize(), "Age_Weeks": age_weeks}

    # 1) Check CHICKEN_FRAMES for a direct recommendation / stage
    frame = CHICKEN_FRAMES.get(chicken_type.capitalize())
    stage_info = {}
    if frame:
        # try to find which stage matches age_weeks by checking Age_Stage content
        age_stage = frame.get("Age_Stage", {})
        # Age_Stage values are strings like "0-8" or nested; try parsing flexibly
        for slot, val in age_stage.items():
            # val might be "0-8" or "0-1.5" weeks — parse numbers
            try:
                parts = val.split("-")
                low = float(parts[0])
                high = float(parts[1])
                # convert weeks possibly floats to int weeks comparison
                if low <= age_weeks <= high:
                    stage_info = {"stage_slot": slot, "stage_range": val}
                    break
            except Exception:
                continue

    # 2) Apply production rules
    rules_out = apply_rules(facts)

    # 3) Gather a recommended feed (from rules or frames)
    recommendation = {}
    if rules_out:
        # merge results - prefer Recommend key
        for r in rules_out:
            if "Recommend" in r:
                recommendation["feed"] = r["Recommend"]
            if "DCP" in r:
                recommendation["dcp"] = r["DCP"]
            if "Warning" in r:
                recommendation.setdefault("warnings", []).append(r["Warning"])

    # If no recommendation yet, fall back to frame recommended feed
    if "feed" not in recommendation and frame:
        recommendation["feed"] = frame.get("Recommended_Feed_Type")
        # if protein range present:
        prange = frame.get("Protein_Requirement_DCP_Range")
        if prange:
            # pick first slot
            first = next(iter(prange.values()))
            recommendation["dcp"] = first

    # 4) Attach recipe if requested and available
    recipe = None
    if include_recipes:
        # find recipe whose Target_Type matches chicken_type
        for rname, rframe in RECIPE_FRAMES.items():
            if rframe.get("Target_Type", "").lower() == chicken_type.lower():
                recipe = {"name": rname, "target_dcp": rframe.get("Target_DCP"), "ingredients": rframe.get("Ingredients")}
                break

    # 5) Final packaging
    return {
        "facts": facts,
        "frame_stage": stage_info,
        "rules_matched": rules_out,
        "recommendation": recommendation,
        "recipe": recipe
    }

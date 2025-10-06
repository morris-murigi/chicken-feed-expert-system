# app/inference_engine.py
from typing import Dict, Any, List, Optional, Tuple
from .knowledge_base import (
    CHICKEN_FRAMES,
    RULES,
    RECIPE_FRAMES,
    INGREDIENT_FRAMES,
)

# ---------- fuzzy helpers ----------
def triangular_membership(x: float, a: float, b: float, c: float) -> float:
    """Simple triangular membership function. Returns degree in [0,1]."""
    if a == b and x == b:
        return 1.0
    if b == c and x == b:
        return 1.0
    if x <= a or x >= c:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a) if (b - a) != 0 else 0.0
    if b <= x < c:
        return (c - x) / (c - b) if (c - b) != 0 else 0.0
    return 0.0


def _get_age_stage_sets_for_frame(frame_key: str) -> Dict[str, Tuple[float, float, float]]:
    """Safely obtain Age_Stage dict for a frame key in CHICKEN_FRAMES."""
    frame = CHICKEN_FRAMES.get(frame_key, {})
    return frame.get("Age_Stage", {}) if isinstance(frame.get("Age_Stage", {}), dict) else {}


def fuzzy_memberships_for_frame(frame_key: str, age_weeks: float) -> Dict[str, float]:
    """Return membership degrees for all labels in frame's Age_Stage."""
    sets = _get_age_stage_sets_for_frame(frame_key)
    memberships = {}
    for label, rng in sets.items():
        try:
            a, b, c = float(rng[0]), float(rng[1]), float(rng[2])
        except Exception:
            try:
                a, b, c = tuple(map(float, rng))
            except Exception:
                memberships[label] = 0.0
                continue
        memberships[label] = round(triangular_membership(age_weeks, a, b, c), 4)
    return memberships


# ---------- type detection ----------
def detect_chicken_type(age_weeks: float, reason: str) -> Dict[str, Any]:
    """Use fuzzy age definitions to detect the best matching chicken frame."""
    reason = (reason or "").strip().lower()
    candidates = []

    if reason == "meat":
        candidate_keys = [k for k in CHICKEN_FRAMES.keys() if "broiler" in k.lower()]
    else:
        candidate_keys = [k for k in CHICKEN_FRAMES.keys() if not ("broiler" in k.lower())]

    if not candidate_keys:
        candidate_keys = list(CHICKEN_FRAMES.keys())

    best_overall = {"frame_key": None, "best_label": None, "degree": 0.0}
    for key in candidate_keys:
        memberships = fuzzy_memberships_for_frame(key, age_weeks)
        if not memberships:
            continue
        label, degree = max(memberships.items(), key=lambda kv: kv[1])
        if degree > best_overall["degree"]:
            best_overall = {"frame_key": key, "best_label": label, "degree": degree}

    # fallback if fuzzy gives 0
    if best_overall["degree"] == 0.0:
        if reason == "meat":
            if age_weeks <= 1.5:
                fk, lbl = "Broiler_starter", "starter"
            elif age_weeks <= 4:
                fk, lbl = "Broiler_grower", "grower"
            else:
                fk, lbl = "Broiler_finisher", "finisher"
        else:
            if age_weeks <= 8:
                fk, lbl = "Chick", "growing"
            elif age_weeks <= 20:
                fk, lbl = "Pullets / Growers", "peak"
            else:
                fk, lbl = "Layer", "productive"
        best_overall = {
            "frame_key": fk if fk in CHICKEN_FRAMES else list(CHICKEN_FRAMES.keys())[0],
            "best_label": lbl,
            "degree": 0.0,
        }
    return best_overall


# ---------- rule engine ----------
def _matches_condition(facts: Dict[str, Any], cond_key: str, cond_val: Any) -> bool:
    """Evaluate a single condition against facts."""
    if cond_key == "Any":
        return True
    if cond_key not in facts:
        return False

    fact_val = facts[cond_key]

    # handle egg production threshold like "<50%"
    if isinstance(cond_val, str) and cond_val.startswith("<"):
        try:
            threshold = float(cond_val.strip("<% "))
            if isinstance(fact_val, str) and fact_val.endswith("%"):
                fact_num = float(fact_val.strip("% "))
            else:
                fact_num = float(fact_val)
            return fact_num < threshold
        except Exception:
            return False

    return fact_val == cond_val


def apply_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evaluate all RULES against provided facts and return matched rules."""
    results = []
    for rule in RULES:
        conditions = rule.get("if", {})
        ok = True
        for k, v in conditions.items():
            if k == "Any":
                continue
            if not _matches_condition(facts, k, v):
                ok = False
                break
        if ok:
            then_part = rule.get("then", {}).copy()
            then_part["_rule"] = rule.get("name")
            results.append(then_part)
    return results


# ---------- recipe & cost ----------
def _find_best_recipe_for_type(chicken_type_label: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """Find best recipe for given chicken type."""
    if not chicken_type_label:
        return None
    target = chicken_type_label.lower()
    for rname, rframe in RECIPE_FRAMES.items():
        tt = (rframe.get("Target_Type") or "").lower()
        if tt == target or target in tt or tt in target:
            return rname, rframe
    for rname, rframe in RECIPE_FRAMES.items():
        if (rframe.get("Target_Type") or "").lower().startswith(target.split()[0]):
            return rname, rframe
    return None


def _get_price_for_ingredient(ingredient_name: str) -> float:
    """Try exact or fuzzy ingredient match for price lookup."""
    if ingredient_name in INGREDIENT_FRAMES:
        return INGREDIENT_FRAMES[ingredient_name].get("Price_per_kg", 0.0)

    candidate = ingredient_name.lower()
    for k, v in INGREDIENT_FRAMES.items():
        if k.lower() == candidate:
            return v.get("Price_per_kg", 0.0)

    for k, v in INGREDIENT_FRAMES.items():
        if candidate in k.lower():
            return v.get("Price_per_kg", 0.0)

    base = ingredient_name.split("(")[0].strip().lower()
    for k, v in INGREDIENT_FRAMES.items():
        if base == k.split("(")[0].strip().lower():
            return v.get("Price_per_kg", 0.0)
    return 0.0


def compute_recipe_cost(recipe_name: str, bag_weight_kg: float = 70.0) -> Dict[str, Any]:
    """Compute cost breakdown for given recipe."""
    r = RECIPE_FRAMES.get(recipe_name)
    if not r:
        return {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}

    breakdown: Dict[str, Dict[str, Any]] = {}
    total_cost = 0.0

    for ing, qty in r.get("Ingredients", {}).items():
        price = _get_price_for_ingredient(ing)
        cost = round(price * float(qty), 2)
        breakdown[ing] = {"qty_kg": float(qty), "price_per_kg": price, "cost": cost}
        total_cost += cost

    total_cost = round(total_cost, 2)
    cost_per_kg = round(total_cost / bag_weight_kg, 2) if bag_weight_kg > 0 else 0.0
    return {"ingredients": breakdown, "total_cost": total_cost, "cost_per_kg": cost_per_kg}


# ---------- main API ----------
def recommend_feed(
    age_weeks: float,
    reason: str = "Eggs",
    budget: str = "optimum",
    egg_production: Optional[Any] = None,
    health: Optional[str] = None,
    feed_cost_tag: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Core inference entry used by FastAPI.
    """
    reason = (reason or "Eggs").strip()
    budget = (budget or "optimum").strip().lower()

    detection = detect_chicken_type(age_weeks, reason)
    frame_key = detection.get("frame_key")
    best_label = detection.get("best_label")
    degree = detection.get("degree", 0.0)

    facts: Dict[str, Any] = {
        "Type": frame_key,
        "Age_Weeks": age_weeks,
        "Reason": reason,
    }
    if best_label:
        facts["Age_Fuzzy"] = best_label
    if egg_production is not None:
        if isinstance(egg_production, (int, float)):
            facts["EggProduction"] = f"{egg_production}%"
        else:
            facts["EggProduction"] = str(egg_production)
    if health:
        facts["Health"] = health
    if feed_cost_tag:
        facts["FeedCost"] = feed_cost_tag

    matched = apply_rules(facts)

    recommended_type = None
    for then in matched:
        if "Recommend" in then:
            recommended_type = then["Recommend"]
            break

    if not recommended_type:
        frame = CHICKEN_FRAMES.get(frame_key, {})
        recommended_type = frame.get("Recommended_Feed_Type")

    recipe_info = None
    recipe_name = None
    if budget == "optimum" and recommended_type:
        found = _find_best_recipe_for_type(recommended_type)
        if found:
            recipe_name, recipe_info = found
            cost_detail = compute_recipe_cost(recipe_name)
        else:
            cost_detail = {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}
    else:
        cost_detail = {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}
        if budget == "low":
            already = any("Alternative Feed Mix" in str(r.get("Recommend", "")) for r in matched)
            if not already:
                matched.append({
                    "Recommend": "Alternative Feed Mix",
                    "Advice": "Use maize bran + fishmeal as cheaper substitute.",
                    "_rule": "R_emergency_filler",
                })

    return {
        "facts": facts,
        "detected_frame": frame_key,
        "detected_age_label": best_label,
        "detected_degree": degree,
        "recommendations": matched,
        "recommended_feed_type": recommended_type,
        "recipe_name": recipe_name,
        "recipe_frame": recipe_info,
        "cost_breakdown": cost_detail,
    }


def get_feed_recipe(feed_type: Optional[str]) -> Dict[str, Any]:
    """Wrapper for external code that needs recipe lookup."""
    if not feed_type:
        return {}
    found = _find_best_recipe_for_type(feed_type)
    return {"name": found[0], "frame": found[1]} if found else {}

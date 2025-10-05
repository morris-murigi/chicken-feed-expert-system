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

def _get_age_stage_sets_for_frame(frame_key: str) -> Dict[str, Tuple[float,float,float]]:
    """
    Safely obtain Age_Stage dict for a frame key in CHICKEN_FRAMES.
    Returns empty dict if not present.
    """
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
            # if a tuple is provided as ints or floats already, handle
            try:
                a, b, c = tuple(map(float, rng))
            except Exception:
                memberships[label] = 0.0
                continue
        memberships[label] = round(triangular_membership(age_weeks, a, b, c), 4)
    return memberships

# ---------- type detection ----------
def detect_chicken_type(age_weeks: float, reason: str) -> Dict[str, Any]:
    """
    Use fuzzy age definitions in CHICKEN_FRAMES to detect the best matching chicken frame.
    If reason == "meat" prefer broiler frames only.
    Returns dictionary: {"frame_key": ..., "best_label": ..., "degree": ...}
    """
    reason = (reason or "").strip().lower()
    candidates = []

    # build candidate frame keys depending on reason
    if reason == "meat":
        # prefer broiler frames
        candidate_keys = [k for k in CHICKEN_FRAMES.keys() if "broiler" in k.lower()]
    else:
        # prefer chick/grower/layer/kienyeji
        candidate_keys = [k for k in CHICKEN_FRAMES.keys() if not ("broiler" in k.lower())]

    # if nothing found (odd KB structure), fallback to all frames
    if not candidate_keys:
        candidate_keys = list(CHICKEN_FRAMES.keys())

    best_overall = {"frame_key": None, "best_label": None, "degree": 0.0}
    for key in candidate_keys:
        memberships = fuzzy_memberships_for_frame(key, age_weeks)
        if not memberships:
            continue
        # use the maximum membership label for this frame
        label, degree = max(memberships.items(), key=lambda kv: kv[1])
        if degree > best_overall["degree"]:
            best_overall = {"frame_key": key, "best_label": label, "degree": degree}

    # If degree is zero, fall back to simple crisp mapping by numeric ranges (safe fallback)
    if best_overall["degree"] == 0.0:
        # simple fallback: map by numeric cutoffs commonly used
        if reason == "meat":
            if age_weeks <= 1.5:
                fk = "Broiler_starter"
                lbl = "starter"
            elif age_weeks <= 4:
                fk = "Broiler_grower"
                lbl = "grower"
            else:
                fk = "Broiler_finisher"
                lbl = "finisher"
        else:
            if age_weeks <= 8:
                fk = "Chick"
                lbl = "growing"
            elif age_weeks <= 20:
                fk = "Pullets / Growers"
                lbl = "peak"
            else:
                fk = "Layer"
                lbl = "productive"
        best_overall = {"frame_key": fk if fk in CHICKEN_FRAMES else list(CHICKEN_FRAMES.keys())[0],
                        "best_label": lbl, "degree": 0.0}
    return best_overall

# ---------- rule engine ----------
def _matches_condition(facts: Dict[str, Any], cond_key: str, cond_val: Any) -> bool:
    """
    Evaluate a single condition against facts.
    Handles:
      - 'Any' key (ignored by caller)
      - Age_Fuzzy equality (string)
      - EggProduction strings like "<50%"
      - standard exact equality
    """
    if cond_key == "Any":
        return True
    if cond_key not in facts:
        return False

    fact_val = facts[cond_key]

    # handle egg production threshold expressed as "<50%"
    if isinstance(cond_val, str) and cond_val.startswith("<"):
        # try to parse numeric from both sides
        try:
            threshold = float(cond_val.strip("<% "))
            # allow fact_val as "45%" or numeric
            if isinstance(fact_val, str) and fact_val.endswith("%"):
                fact_num = float(fact_val.strip("% "))
            else:
                fact_num = float(fact_val)
            return fact_num < threshold
        except Exception:
            return False

    # plain equality for Age_Fuzzy and other string fields
    return fact_val == cond_val

def apply_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluate all RULES against provided facts and return list of 'then' dicts
    for rules that match. Keeps order — caller can use priority keys if needed.
    """
    results = []
    for rule in RULES:
        conditions = rule.get("if", {})
        # check all conditions
        ok = True
        for k, v in conditions.items():
            if k == "Any":
                continue
            if not _matches_condition(facts, k, v):
                ok = False
                break
        if ok:
            then_part = rule.get("then", {}).copy()
            # include rule name for traceability
            then_part["_rule"] = rule.get("name")
            results.append(then_part)
    return results

# ---------- recipe & cost ----------
def _find_best_recipe_for_type(chicken_type_label: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Find a recipe name+frame whose Target_Type best matches the given chicken type label.
    Matching uses lower-case substring equality to be tolerant.
    Returns (recipe_name, recipe_frame) or None.
    """
    if not chicken_type_label:
        return None
    target = chicken_type_label.lower()
    for rname, rframe in RECIPE_FRAMES.items():
        tt = (rframe.get("Target_Type") or "").lower()
        # allow exact or substring match
        if tt == target or target in tt or tt in target:
            return rname, rframe
    # last resort: try simple startswith match
    for rname, rframe in RECIPE_FRAMES.items():
        if (rframe.get("Target_Type") or "").lower().startswith(target.split()[0]):
            return rname, rframe
    return None

def _get_price_for_ingredient(ingredient_name: str) -> float:
    """Try exact lookup, then several fallbacks (strip parentheses, shorter tokens)."""
    if ingredient_name in INGREDIENT_FRAMES:
        return INGREDIENT_FRAMES[ingredient_name].get("Price_per_kg", 0.0)
    # try normalized matches
    candidate = ingredient_name.lower()
    for k, v in INGREDIENT_FRAMES.items():
        if k.lower() == candidate:
            return v.get("Price_per_kg", 0.0)
    # try substring matching (e.g., "fishmeal" matches "Fishmeal (Omena)")
    for k, v in INGREDIENT_FRAMES.items():
        if candidate in k.lower():
            return v.get("Price_per_kg", 0.0)
    # try removing parenthesis content
    base = ingredient_name.split("(")[0].strip().lower()
    for k, v in INGREDIENT_FRAMES.items():
        if base == k.split("(")[0].strip().lower():
            return v.get("Price_per_kg", 0.0)
    return 0.0

def compute_recipe_cost(recipe_name: str, bag_weight_kg: float = 70.0) -> Dict[str, Any]:
    """
    Return per-ingredient breakdown and total cost for a bag sized bag_weight_kg.
    Assumes the recipe quantities in RECIPE_FRAMES are for the standard bag (70kg).
    """
    r = RECIPE_FRAMES.get(recipe_name)
    if not r:
        return {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}

    breakdown: Dict[str, Dict[str, Any]] = {}
    total_cost = 0.0
    # assume recipe quantities are in kg amounts for 70kg bag
    for ing, qty in r.get("Ingredients", {}).items():
        # qty is given per 70kg bag in your KB
        price = _get_price_for_ingredient(ing)
        cost = round(price * float(qty), 2)
        breakdown[ing] = {"qty_kg": float(qty), "price_per_kg": price, "cost": cost}
        total_cost += cost

    total_cost = round(total_cost, 2)
    cost_per_kg = round(total_cost / bag_weight_kg, 2) if bag_weight_kg > 0 else 0.0
    return {"ingredients": breakdown, "total_cost": total_cost, "cost_per_kg": cost_per_kg}

# ---------- public API ----------
def recommend_feed(
    age_weeks: float,
    reason: str = "Eggs",
    budget: str = "optimum",
    egg_production: Optional[Any] = None,
    health: Optional[str] = None,
    feed_cost_tag: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Top-level function used by the API.
    - age_weeks: numeric weeks
    - reason: "Eggs" or "Meat"
    - budget: "optimum" or "low"
    - egg_production: optional numeric or "NN%" string
    - health: optional "Healthy"/"Sick"
    - feed_cost_tag: optional string passed to facts (e.g., "High")
    Returns a dict with: facts, detected_type, matched_rules (recommendations), recipe (name/frame),
    and cost_breakdown (ingredients + total) when applicable.
    """
    # normalize inputs
    reason = (reason or "Eggs").strip()
    budget = (budget or "optimum").strip().lower()

    detection = detect_chicken_type(age_weeks, reason)
    frame_key = detection.get("frame_key")
    best_label = detection.get("best_label")
    degree = detection.get("degree", 0.0)

    # build facts for rule evaluation
    facts: Dict[str, Any] = {
        "Type": frame_key,
        "Age_Weeks": age_weeks,
        "Reason": reason,
    }
    if best_label:
        facts["Age_Fuzzy"] = best_label
    if egg_production is not None:
        # store as string with percent if numeric provided
        if isinstance(egg_production, (int, float)):
            facts["EggProduction"] = f"{egg_production}%"
        else:
            facts["EggProduction"] = str(egg_production)
    if health:
        facts["Health"] = health
    if feed_cost_tag:
        facts["FeedCost"] = feed_cost_tag

    # apply rules (these will use Age_Fuzzy and other facts)
    matched = apply_rules(facts)

    # choose primary recommendation (first Recommend in matched), else fall back to frame Recommended_Feed_Type
    recommended_type = None
    for then in matched:
        if "Recommend" in then:
            recommended_type = then["Recommend"]
            break

    if not recommended_type:
        # fallback: use the frame's Recommended_Feed_Type if available
        frame = CHICKEN_FRAMES.get(frame_key, {})
        recommended_type = frame.get("Recommended_Feed_Type")

    # map recommended_type to recipe (best effort)
    recipe_info = None
    recipe_name = None
    if budget == "optimum" and recommended_type:
        found = _find_best_recipe_for_type(recommended_type)
        if found:
            recipe_name, recipe_info = found
            cost_detail = compute_recipe_cost(recipe_name)
        else:
            recipe_name = None
            recipe_info = None
            cost_detail = {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}
    else:
        # low budget: do not compute full recipe; append emergency filler recommendation if rule not already present
        cost_detail = {"ingredients": {}, "total_cost": 0.0, "cost_per_kg": 0.0}
        if budget == "low":
            # ensure emergency filler recommendation exists in results
            already = any("Alternative Feed Mix" in str(r.get("Recommend", "")) for r in matched)
            if not already:
                matched.append({
                    "Recommend": "Alternative Feed Mix",
                    "Advice": "Use maize bran + fishmeal as cheaper substitute.",
                    "_rule": "R_emergency_filler"
                })

    output = {
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
    return output

# convenience small wrapper for old code that expected apply_rules/get_feed_recipe:
def get_feed_recipe(feed_type: Optional[str]) -> Dict[str, Any]:
    if not feed_type:
        return {}
    found = _find_best_recipe_for_type(feed_type)
    return {"name": found[0], "frame": found[1]} if found else {}

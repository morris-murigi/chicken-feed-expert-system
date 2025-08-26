from typing import Dict, Any, List
from app.knowledge_base import RULES, CHICKEN_FRAMES, RECIPE_FRAMES

def apply_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evaluate all rules against provided facts and return applicable recommendations"""
    results = []
    for rule in RULES:
        conditions = rule.get("if", {})
        match = True

        for key, value in conditions.items():
            if key == "Any":  # global rules
                continue
            if key not in facts:
                match = False
                break
            fact_value = facts[key]
            if isinstance(value, tuple):  # age ranges
                if not (value[0] <= fact_value <= value[1]):
                    match = False
                    break
            elif isinstance(value, str) and value.startswith("<"):
                # e.g. "<50%"
                try:
                    threshold = float(value.strip("<%"))
                    fact_num = float(str(fact_value).strip("%"))
                    if not fact_num < threshold:
                        match = False
                        break
                except:
                    match = False
                    break
            else:
                if fact_value != value:
                    match = False
                    break

        if match:
            results.append(rule.get("then", {}))

    return results


def get_feed_recipe(feed_type: str) -> Dict[str, Any]:
    """Fetch matching recipe by feed type"""
    for recipe_name, recipe in RECIPE_FRAMES.items():
        if recipe["Target_Type"].lower() == feed_type.lower():
            return recipe
    return {}

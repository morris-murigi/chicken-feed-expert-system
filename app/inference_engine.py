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

import numpy as np

def triangular_membership(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership function"""
    if a <= x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b <= x <= c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0


def fuzzify(value: float, fuzzy_sets: Dict[str, tuple]) -> Dict[str, float]:
    """Return membership degrees of a value across fuzzy sets"""
    memberships = {}
    for label, (a, b, c) in fuzzy_sets.items():
        memberships[label] = round(triangular_membership(value, a, b, c), 2)
    return memberships

from app.knowledge_base import FUZZY_SETS

def fuzzy_recommend_feed(age_weeks: float, protein: float = None, cost: float = None):
    """Fuzzy evaluation of feed suitability"""
    age_membership = fuzzify(age_weeks, FUZZY_SETS["Age"])
    
    # Example fuzzy rule base (simplified)
    # If Chick AND High Protein AND Cheap → High Suitability
    # If Grower AND Medium Protein AND Cheap → Medium Suitability
    # If Expensive AND Low Protein → Low Suitability
    
    suitability = []
    
    if age_membership["Chick"] > 0:
        score = 0.6 + 0.4 * age_membership["Chick"]
        suitability.append(("Chick Mash", round(score, 2)))
    
    if age_membership["Grower"] > 0:
        score = 0.5 + 0.5 * age_membership["Grower"]
        suitability.append(("Grower Mash", round(score, 2)))
    
    if age_membership["Layer"] > 0:
        score = 0.7 + 0.3 * age_membership["Layer"]
        suitability.append(("Layer Mash", round(score, 2)))

    # Pick the highest suitability feed
    if suitability:
        best = max(suitability, key=lambda x: x[1])
        return {"age_membership": age_membership, "options": suitability, "recommended": best}
    else:
        return {"error": "No fuzzy match found"}
print(fuzzy_recommend_feed(7))   # 7-week chick
print(fuzzy_recommend_feed(10))  # 10-week grower
print(fuzzy_recommend_feed(25))  # 25-week layer

def fuzzy_recommend_broiler(age_weeks: float, protein: float = 22.0):
    """Fuzzy recommendation for broiler feed phases"""
    age_membership = fuzzify(age_weeks, FUZZY_SETS["Broiler_Age"])
    protein_membership = fuzzify(protein, FUZZY_SETS["Broiler_Protein"])

    suitability = []

    # Fuzzy rules
    if age_membership["Starter"] > 0:
        score = 0.6 + 0.4 * age_membership["Starter"]
        suitability.append(("Broiler Starter", round(score, 2)))

    if age_membership["Grower"] > 0:
        score = 0.5 + 0.5 * age_membership["Grower"]
        suitability.append(("Broiler Grower", round(score, 2)))

    if age_membership["Finisher"] > 0:
        score = 0.7 + 0.3 * age_membership["Finisher"]
        suitability.append(("Broiler Finisher", round(score, 2)))

    # Adjust score if protein is too low
    if protein_membership["Low"] > 0:
        suitability = [(f, round(s - 0.2, 2)) for f, s in suitability]

    # Pick the best feed
    if suitability:
        best = max(suitability, key=lambda x: x[1])
        return {
            "age_membership": age_membership,
            "protein_membership": protein_membership,
            "options": suitability,
            "recommended": best
        }
    else:
        return {"error": "No fuzzy match found"}
print(fuzzy_recommend_broiler(1))   # 1 week old chick
print(fuzzy_recommend_broiler(2.5)) # 2.5 weeks old
print(fuzzy_recommend_broiler(5))   # 5 weeks old

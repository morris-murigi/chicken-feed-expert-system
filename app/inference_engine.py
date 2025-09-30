from app.knowledge_base import rules, recipes

def apply_rules(facts):
    recommendations = []
    for rule in rules:
        conditions_met = True
        for key, condition in rule["conditions"].items():
            if key in facts:
                value = facts[key]
                if isinstance(condition, dict):
                    operator = condition.get("operator")
                    condition_value = condition.get("value")
                    if value is None:
                        conditions_met = False
                        continue
                    if operator == "<=" and value > condition_value:
                        conditions_met = False
                    elif operator == ">" and value <= condition_value:
                        conditions_met = False
                    elif operator == ">=" and value < condition_value:
                        conditions_met = False
                    elif operator == "<" and value >= condition_value:
                        conditions_met = False
                    if "operator2" in condition and "value2" in condition:
                        operator2 = condition.get("operator2")
                        value2 = condition.get("value2")
                        if operator2 == "<=" and value > value2:
                            conditions_met = False
                        elif operator2 == ">" and value <= value2:
                            conditions_met = False
                else:
                    if value != condition:
                        conditions_met = False
            else:
                conditions_met = False
            if not conditions_met:
                break
        if conditions_met:
            recommendations.append(rule["consequence"])
    return recommendations if recommendations else [{"Recommend": facts["Type"], "Target_DCP": "Default"}]

def get_feed_recipe(feed_type):
    return recipes.get(feed_type, {"name": f"{feed_type} Default Feed", "target_dcp": "N/A", "ingredients": {}})

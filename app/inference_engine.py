from app.knowledge_base import rules, recipes

def apply_rules(facts):
    recommendations = []
    for rule in rules:
        conditions_met = True
        for key, condition in rule["conditions"].items():
            if key in facts:
                value = facts[key]
                operator = condition["operator"]
                condition_value = condition["value"]
                if operator == "<=":
                    if value > condition_value:
                        conditions_met = False
                elif operator == ">":
                    if value <= condition_value:
                        conditions_met = False
                elif operator == ">=":
                    if value < condition_value:
                        conditions_met = False
                elif operator == "<":
                    if value >= condition_value:
                        conditions_met = False
                # Add more operators as needed
            else:
                conditions_met = False
            if not conditions_met:
                break
        if conditions_met:
            recommendations.append(rule["consequence"])
    return recommendations

def get_feed_recipe(feed_type):
    return recipes.get(feed_type, {})

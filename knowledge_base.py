# knowledge_base.py

# Frame representation of chicken feed knowledge
knowledge_base = {
    "broiler": {
        "starter": {
            "age_days": (0, 21),
            "feed": "Broiler Starter Mash",
            "protein": "22%",
            "energy": "3000 kcal/kg",
            "notes": "Ensure constant clean water supply and maintain brooder temperature."
        },
        "grower": {
            "age_days": (22, 35),
            "feed": "Broiler Grower Mash",
            "protein": "20%",
            "energy": "3100 kcal/kg",
            "notes": "Provide enough feeding space to avoid competition."
        },
        "finisher": {
            "age_days": (36, 45),
            "feed": "Broiler Finisher Mash",
            "protein": "18%",
            "energy": "3200 kcal/kg",
            "notes": "Withhold feed 8 hours before slaughter to reduce gut content."
        }
    },
    "layer": {
        "chick": {
            "age_days": (0, 56),
            "feed": "Chick Mash",
            "protein": "20%",
            "energy": "2800 kcal/kg",
            "notes": "Keep heat and ventilation balanced to avoid stress."
        },
        "grower": {
            "age_days": (57, 140),
            "feed": "Grower Mash",
            "protein": "18%",
            "energy": "2900 kcal/kg",
            "notes": "Avoid excess energy to prevent obesity."
        },
        "layer": {
            "age_days": (141, 500),
            "feed": "Layer Mash",
            "protein": "16%",
            "energy": "2800 kcal/kg",
            "notes": "Provide calcium supplements for strong eggshells."
        }
    }
}

def get_feed_recommendation(chicken_type, age_days):
    """Return feed recommendation based on chicken type and age."""
    if chicken_type not in knowledge_base:
        return None

    for stage, data in knowledge_base[chicken_type].items():
        min_age, max_age = data["age_days"]
        if min_age <= age_days <= max_age:
            return {
                "stage": stage,
                "feed": data["feed"],
                "protein": data["protein"],
                "energy": data["energy"],
                "notes": data["notes"]
            }
    return None

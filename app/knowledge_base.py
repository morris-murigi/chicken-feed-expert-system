recipes = {
    "Chick": {
        "name": "Chick Starter Feed",
        "target_dcp": "20-24% protein",
        "ingredients": {
            "Corn": 60,
            "Soybean Meal": 35,
            "Limestone": 3,
            "Vitamin Premix": 2
        }
    },
    "Pullets / Growers": {
        "name": "Grower Feed",
        "target_dcp": "16-18% protein",
        "ingredients": {
            "Corn": 65,
            "Soybean Meal": 30,
            "Limestone": 3,
            "Vitamin Premix": 2
        }
    },
    "Layer": {
        "name": "Layer Feed",
        "target_dcp": "16% protein",
        "ingredients": {
            "Corn": 60,
            "Soybean Meal": 25,
            "Limestone": 10,
            "Vitamin Premix": 5
        }
    },
    "Broiler Starter": {
        "name": "Broiler Starter Feed",
        "target_dcp": "22% protein",
        "ingredients": {
            "Corn": 55,
            "Soybean Meal": 40,
            "Limestone": 3,
            "Vitamin Premix": 2
        }
    },
    "Broiler Grower": {
        "name": "Broiler Grower Feed",
        "target_dcp": "20% protein",
        "ingredients": {
            "Corn": 60,
            "Soybean Meal": 35,
            "Limestone": 3,
            "Vitamin Premix": 2
        }
    },
    "Broiler Finisher": {
        "name": "Broiler Finisher Feed",
        "target_dcp": "18% protein",
        "ingredients": {
            "Corn": 65,
            "Soybean Meal": 30,
            "Limestone": 3,
            "Vitamin Premix": 2
        }
    }
}

rules = [
    # Chick rules
    {"conditions": {"Type": "Chick", "Age_Weeks": {"operator": "<=", "value": 8}},
     "consequence": {"Recommend": "Chick", "Target_DCP": "20-24%"}},
    # Pullets / Growers rules
    {"conditions": {"Type": "Pullets / Growers", "Age_Weeks": {"operator": ">", "value": 8}},
     "consequence": {"Recommend": "Pullets / Growers", "Target_DCP": "16-18%"}},
    # Layer rules
    {"conditions": {"Type": "Layer", "Age_Weeks": {"operator": ">=", "value": 18}},
     "consequence": {"Recommend": "Layer", "Target_DCP": "16%"}},
    # Broiler Starter rules
    {"conditions": {"Type": "Broiler Starter", "Age_Weeks": {"operator": "<=", "value": 3}},
     "consequence": {"Recommend": "Broiler Starter", "Target_DCP": "22%"}},
    # Broiler Grower rules
    {"conditions": {"Type": "Broiler Grower", "Age_Weeks": {"operator": ">", "value": 3, "operator2": "<=", "value2": 6}},
     "consequence": {"Recommend": "Broiler Grower", "Target_DCP": "20%"}},
    # Broiler Finisher rules
    {"conditions": {"Type": "Broiler Finisher", "Age_Weeks": {"operator": ">", "value": 6}},
     "consequence": {"Recommend": "Broiler Finisher", "Target_DCP": "18%"}},
    # Additional rules for optional fields (EggProduction, FeedCost, Health)
    {"conditions": {"EggProduction": {"operator": "<", "value": "70%"}},
     "consequence": {"Warnings": "Low egg production. Consider adjusting feed."}},
    {"conditions": {"FeedCost": "High"},
     "consequence": {"Recommend": "Premium Feed"}},
    {"conditions": {"Health": "Sick"},
     "consequence": {"Warnings": "Consult a vet. Adjust feed for recovery."}},
]

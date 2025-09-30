recipes = {
    "Broiler Starter": {
        "name": "Broiler Starter Feed (1-4 weeks)",
        "target_dcp": "22% protein",
        "ingredients": {
            "Whole Maize": 40,
            "Fishmeal (Omena)": 12,
            "Soya Bean Meal": 14,
            "Lime": 4,
            "Premix": 0.07,
            "Salt": 0.04,
            "Coccidiostat": 0.005,
            "Zincbacitrach": 0.005
        }
    },
    "Broiler Grower": {
        "name": "Broiler Grower Feed",
        "target_dcp": "20% protein",
        "ingredients": {
            "Whole Maize": 10,
            "Wheat Bran": 16.7,
            "Sunflower/Cotton Seed": 13.3,
            "Fishmeal": 10,
            "Lime": 15,
            "Premix": 0.07,
            "Salt": 0.04,
            "Coccidiostat": 0.005,
            "Zincbacitrach": 0.005
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
    },
    "Chick": {
        "name": "Chick and Duck Mash (0-8 weeks)",
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
    }
}

rules = [
    {"conditions": {"Type": "Broiler Starter", "Age_Weeks": {"operator": "<=", "value": 4}}, "consequence": {"Recommend": "Broiler Starter", "Target_DCP": "22% protein"}},
    {"conditions": {"Type": "Broiler Grower", "Age_Weeks": {"operator": ">", "value": 4, "operator2": "<=", "value2": 6}}, "consequence": {"Recommend": "Broiler Grower", "Target_DCP": "20% protein"}},
    {"conditions": {"Type": "Broiler Finisher", "Age_Weeks": {"operator": ">", "value": 6}}, "consequence": {"Recommend": "Broiler Finisher", "Target_DCP": "18% protein"}},
    {"conditions": {"Type": "Chick", "Age_Weeks": {"operator": "<=", "value": 8}}, "consequence": {"Recommend": "Chick", "Target_DCP": "20-24% protein"}},
    {"conditions": {"Type": "Pullets / Growers", "Age_Weeks": {"operator": ">", "value": 8}}, "consequence": {"Recommend": "Pullets / Growers", "Target_DCP": "16-18% protein"}},
    {"conditions": {"Type": "Layer", "Age_Weeks": {"operator": ">=", "value": 18}}, "consequence": {"Recommend": "Layer", "Target_DCP": "16% protein"}},
    {"conditions": {"EggProduction": {"operator": "<", "value": "70%"}}, "consequence": {"Warnings": "Low egg production. Consider adjusting feed."}},
    {"conditions": {"FeedCost": "High"}, "consequence": {"Recommend": "Premium Feed"}},
    {"conditions": {"Health": "Sick"}, "consequence": {"Warnings": "Consult a vet. Adjust feed for recovery."}},
]

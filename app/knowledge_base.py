recipes = {
    "Chick": {
        "name": "Chick Starter Feed",
        "target_dcp": "20-24% protein",
        "ingredients": {"Corn": 60, "Soybean Meal": 35, "Limestone": 3, "Vitamin Premix": 2}
    },
    "Pullets / Growers": {
        "name": "Grower Feed",
        "target_dcp": "16-18% protein",
        "ingredients": {"Corn": 65, "Soybean Meal": 30, "Limestone": 3, "Vitamin Premix": 2}
    },
    "Layer": {
        "name": "Layer Feed",
        "target_dcp": "16% protein",
        "ingredients": {"Corn": 60, "Soybean Meal": 25, "Limestone": 10, "Vitamin Premix": 5}
    },
    "Broiler Starter": {
        "name": "Broiler Starter Feed",
        "target_dcp": "22% protein",
        "ingredients": {"Corn": 55, "Soybean Meal": 40, "Limestone": 3, "Vitamin Premix": 2}
    },
    "Broiler Grower": {
        "name": "Broiler Grower Feed",
        "target_dcp": "20% protein",
        "ingredients": {"Corn": 60, "Soybean Meal": 35, "Limestone": 3, "Vitamin Premix": 2}
    },
    "Broiler Finisher": {
        "name": "Broiler Finisher Feed",
        "target_dcp": "18% protein",
        "ingredients": {"Corn": 65, "Soybean Meal": 30, "Limestone": 3, "Vitamin Premix": 2}
    }
}

rules = [
    {"conditions": {"Type": "Chick", "Age_Weeks": {"operator": "<=", "value": 8}}, "consequence": {"Recommend": "Chick"}},
    {"conditions": {"Type": "Pullets / Growers", "Age_Weeks": {"operator": ">", "value": 8}}, "consequence": {"Recommend": "Pullets / Growers"}},
    {"conditions": {"Type": "Layer", "Age_Weeks": {"operator": ">=", "value": 18}}, "consequence": {"Recommend": "Layer"}},
    {"conditions": {"Type": "Broiler Starter", "Age_Weeks": {"operator": "<=", "value": 3}}, "consequence": {"Recommend": "Broiler Starter"}},
    {"conditions": {"Type": "Broiler Grower", "Age_Weeks": {"operator": ">", "value": 3, "operator2": "<=", "value2": 6}}, "consequence": {"Recommend": "Broiler Grower"}},
    {"conditions": {"Type": "Broiler Finisher", "Age_Weeks": {"operator": ">", "value": 6}}, "consequence": {"Recommend": "Broiler Finisher"}},
]

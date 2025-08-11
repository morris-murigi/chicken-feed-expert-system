# app/knowledge_base.py

# 1. SEMANTICS (Core concepts and relationships)
SEMANTICS = {
    "Poultry_Feed": {
        "components": ["Grains", "Protein Supplements", "Mineral Supplements", "Vitamin Supplements"],
        "influenced_by": ["Weight", "Age", "Growth Rate", "Egg Production Rate", "Weather", "Foraging Amount"]
    },
    "Chicken_Type": ["Chick", "Pullet", "Layer", "Broiler", "Kienyeji"],
    "Nutritional_Requirements": {
        "Protein": "Amino acids (lysine, methionine, tryptophan, threonine)",
        "Carbohydrates": "Energy source",
        "Vitamins": ["A", "D", "E", "K", "B-complex"],
        "Minerals": ["Ca", "P", "Na", "Zn", "Cu", "Fe", "Mn", "I"],
        "Water": "Essential"
    },
    "Feed_Ingredient": [
        "Whole Maize", "Soya Bean Meal", "Fishmeal (Omena)", "Wheat Bran", "Sunflower Cake", 
        "Cotton Seed Cake", "Lime", "Salt", "Premix", "Enzymes", "Coccidiostat", "Toxin Binder"
    ],
    "Feed_Formulation_Method": ["Pearson Square Method", "Crude Protein Calculation"],
    "Feed_Management": ["Feeder Types", "Feeding Frequency", "Wastage Control", "Storage Conditions"],
    "Quality_Control": ["Ingredient Quality Checks", "Mixing Methods", "Experimental Trials"],
    "Inventory_Management": ["Stock Tracking", "Reorder Alerts", "Spoilage Monitoring"]
}

# 2. FRAMES (Structured slot-and-filler)
CHICKEN_FRAMES = {
    "Chick": {
        "Age_Stage": {"Starter_Phase_Weeks": "0-8"},
        "Primary_Goal": "Growth",
        "Recommended_Feed_Type": "Chick/Duck Mash",
        "Protein_Requirement_DCP_Range": {"Starter_DCP": "20-22%"},
        "Daily_Feed_Consumption_g": 40,
        "Total_Feed_Per_Stage_kg": 2.0
    },
    "Layer": {
        "Age_Stage": {"Layer_Phase_Weeks": "18-76"},
        "Primary_Goal": "Egg Production",
        "Recommended_Feed_Type": "Layers' Mash",
        "Protein_Requirement_DCP_Range": {"Layer_DCP": "15-18%"},
        "Calcium_Requirement": "High",
        "Daily_Feed_Consumption_g": 125,
        "Total_Feed_Per_Stage_kg": 45
    },
    "Broiler": {
        "Age_Stage": {
            "Starter_Phase_Weeks": "0-1.5",
            "Grower_Phase_Weeks": "1.5-4",
            "Finisher_Phase_Weeks": "4-7"
        },
        "Primary_Goal": "Meat Production",
        "Recommended_Feed_Type": "Broiler Starter/Grower/Finisher",
        "Protein_Requirement_DCP_Range": {"Starter_DCP": "22-24%"},
        "Daily_Feed_Consumption_g": None,
        "Total_Feed_Per_Stage_kg": 4.5
    }
}

INGREDIENT_FRAMES = {
    "Whole Maize": {"Type": "Grain", "CP%": 8.23, "Prep": "Milling", "QC": "Avoid mold"},
    "Soya Bean Meal": {"Type": "Protein Supplement", "CP%": 45, "Prep": "None", "QC": "Dry, no pests"},
    "Fishmeal (Omena)": {"Type": "Protein Supplement", "CP%": 55, "Prep": "None", "QC": "No sand/seashells"}
}

RECIPE_FRAMES = {
    "70kg Chick Mash": {
        "Target_Type": "Chick",
        "Target_DCP": "20%",
        "Ingredients": {
            "Whole Maize": 31.5,
            "Wheat Bran": 9.1,
            "Wheat Pollard": 7.0,
            "Sunflower": 16.8,
            "Fishmeal": 1.5,
            "Lime": 1.75,
            "Salt": 0.03,
            "Premix": 0.02
        }
    }
}

# 3. RULES (Production Rules)
RULES = [
    {
        "name": "R_Feed_Type_Chicks",
        "if": {"Age_Weeks": (0, 8)},
        "then": {"Recommend": "Chick/Duck Mash", "DCP": "20-22%"}
    },
    {
        "name": "R_Layer_Calcium_Warning",
        "if": {"Type": "Layer", "Age_Weeks": (0, 18)},
        "then": {"Warning": "High calcium damages kidneys"}
    }
]

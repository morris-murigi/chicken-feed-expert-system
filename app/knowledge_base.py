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

# 2. FRAMES 
CHICKEN_FRAMES = {
    "Chick": {
        "Age_Stage": {"Starter_Phase_Weeks": "0-8"},
        "Primary_Goal": "Growth",
        "Recommended_Feed_Type": "Chick/Duck Mash",
        "Protein_Requirement_DCP_Range": {"Starter_DCP": "20-22%"},
        "Daily_Feed_Consumption_g": 40,
        "Total_Feed_Per_chick_kg": 2.0
    },
    "Pullets / Growers":{
        "Age_Stage": {"Grower_Phase_Weeks": "8-20"},
        "Primary_Goal" : "Growth",
        "Recommended_Feed_Type": "Grower Mash",
        "Protein_Requirement_DCP_Range": {"Grower_DCP": "16-18%"},
        "Daily_Feed_Consumption_g" :80, 
        "Total_Feed_Per_bird_kg" : 8.5
    },
    "Layer": {
        "Age_Stage": {"Layer_Phase_Weeks": "20-76"},
        "Primary_Goal": "Egg Production",
        "Recommended_Feed_Type": "Layers' Mash",
        "Protein_Requirement_DCP_Range": {"Layer_DCP": "15-18%"},
        "Calcium_Requirement": "High",
        "Daily_Feed_Consumption_g": 125,
        "Total_Feed_Per_Stage_kg": 45
    },
    "Broiler_starter": {
        "Age_Stage": {"Starter_Phase_Weeks": "0-1.5"},
        "Primary_Goal": "Meat Production",
        "Recommended_Feed_Type": "Broiler Starter",
        "Protein_Requirement_DCP_Range": {"Starter_DCP": "22-24%"},
        "Daily_Feed_Consumption_g": 3,
        "Total_Feed_Per_Stage_kg": 4.5
    },
    "Broiler_grower": {
        "Age_Stage": {"Grower_Phase_Weeks": "1.5-4"},
        "Primary_Goal": "Meat Production",
        "Recommended_Feed_Type": "Broiler Starter",
        "Protein_Requirement_DCP_Range": {"Grower_DCP": "22-24%"},
        "Daily_Feed_Consumption_g": 3,
        "Total_Feed_Per_Stage_kg": 4.5
    },
    "Broiler_finisher": {
        "Age_Stage": {"Finisher_Phase_Weeks": "4-7"},
        "Primary_Goal": "Meat Production",
        "Recommended_Feed_Type": "Broiler Starter",
        "Protein_Requirement_DCP_Range": {"Finisher_DCP": "22-24%"},
        "Daily_Feed_Consumption_g": 3,
        "Total_Feed_Per_Stage_kg": 4.5
    }
}

INGREDIENT_FRAMES = {
    "Whole Maize": {"Type": "Grain", "CP%": 8.23, "Prep": "Milling", "QC": "Avoid mold","Price_per_kg":50 },
    "Soya Bean Meal": {"Type": "Protein Supplement", "CP%": 45, "Prep": "None", "QC": "Dry, no pests","Price_per_kg":84},
    "Fishmeal (Omena)": {"Type": "Protein Supplement", "CP%": 55, "Prep": "None", "QC": "No sand/seashells","Price_per_kg":95},
    "Wheat Bran": {"Type": "Energy & Fiber Source","CP%": 15.2,"Prep": "By-product of milling wheat","QC": "Avoid damp or moldy bran","Price_per_kg":17},
    "Wheat Pollard": {"Type": "Energy Source","CP%": 16.0,"Prep": "By-product of wheat flour milling","QC": "Ensure it is clean, not caked or moldy","Price_per_kg":32},
    "Sunflower": {"Type": "Protein Supplement","CP%": 35,"Prep": "Oil extraction cake","QC": "Avoid rancid-smelling or moldy cakes","Price_per_kg":50},
    "Lime": {"Type": "Mineral Supplement","CP%": 0,"Prep": "Finely ground limestone","QC": "Use food-grade lime, no impurities","Price_per_kg":12},
    "Salt": {"Type": "Mineral Supplement","CP%": 0,"Prep": "None","QC": "Ensure it is free from lumps and impurities","Price_per_kg":50},

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
    },
    "70kg Grower Mash":{
        "Target_Type":"Grower",
        "Target_DCP" :"16-18%",
        "Ingredients":{
            "Whole Maize": 34.0,
            "Wheat Bran": 12.0,
            "Wheat Pollard": 5.0,
            "Sunflower": 10.0,
            "Fishmeal (Omena)": 0.9,
            "Lime": 1.5,
            "Salt": 0.03,
            "Premix": 0.02
        }
    },
    "70kg Layers Mash":{
        "Target_Type":"Layer",
        "Target_DCP" :"15-18%",
        "Ingredients":{
             "Whole Maize": 34.0,
            "Wheat Bran": 10.0,
            "Wheat Pollard": 5.0,
            "Sunflower": 10.0,
            "Fishmeal (Omena)": 1.8,
            "Lime": 3.0,
            "Salt": 0.03,
            "Premix": 0.02
        }
    },
    "70kg Broiler Starter":{
        "Target_Type": "Broiler Starter",
        "Target_DCP": "22-24%",
        "Ingredients": {
            "Whole Maize": 40.0,
            "Soya Bean Meal": 18.0,
            "Fishmeal (Omena)": 7.0,
            "Wheat Bran": 6.0,
            "Lime": 1.0,
            "Salt": 0.25,
            "Premix": 0.25
        }
    },
    "70kg Broiler Grower":{
        "Target_Type": "Broiler Grower",
        "Target_DCP": "20-21%",
        "Ingredients": {
            "Whole Maize": 37.0,
            "Soya Bean Meal": 15.0,
            "Fishmeal (Omena)": 6.0,
            "Wheat Bran": 10.0,
            "Lime": 1.0,
            "Salt": 0.25,
            "Premix": 0.25
        }
    },
    "70kg Broiler Finisher":{
        "Target_Type": "Broiler Finisher",
        "Target_DCP": "18-19%",
        "Ingredients": {
            "Whole Maize": 45.0,
            "Soya Bean Meal": 12.0,
            "Fishmeal (Omena)": 5.0,
            "Wheat Bran": 8.0,
            "Lime": 1.0,
            "Salt": 0.25,
            "Premix": 0.25
        }
    }
}

# 3. RULES (Production Rules)
RULES = [
       {
        "name": "R_Chick_Feed",
        "if": {"Type": "Chick","Age_Weeks": (0, 8)},
        "then": {"Recommend": "Chick/Duck Mash", 
                 "DCP": "20-22%",
                 "Daily_Feed_g": 40,
                 "Advice":"Feed chick mash for growth.  "
                 }
    },
    {
        "name" : "R_Grower_Feed",
        "if":{"Type": "Grower", "Age_Weeks": (8, 20)},
        "then":{"Recommend":"Growers Mash",
                "DCP": "16-18%",
                "Daily_Feed_g": 80,
                "Advice":"Feed growers mash for growth.  "}
    },
    {
        "name" : "R_Layer_Feed",
        "priority": 1,
        "if":{"Type": "Layer", "Age_Weeks": (20,76)},
        "then":{"Recommend":"Layers Mash",
                "DCP": "15-18%",
                "Daily_Feed_g": 125,
                "Advice":"Feed layers mash for growth.  "}
    },
    {
        "name" : "R_Broiler_Starter_Feed",
        "if":{"Type": "Broiler Starter", "Age_Weeks": (0,1.5)},
        "then":{"Recommend":"Broiler Starter Mash",
                "DCP": "22-24%",
                "Daily_Feed_g": 80,
                "Advice":"Feed broiler starter mash for growth.  "}
    },
    {
        "name" : "R_Broiler_Grower_Feed",
        "if":{"Type": "Broiler Grower", "Age_Weeks": (1.5,4)},
        "then":{"Recommend":"Broiler Growers Mash",
                "DCP": "20-21%",
                "Daily_Feed_g": 80,
                "Advice":"Feed broiler grower mash for growth.  "}
    },
    {   "name" : "R_Broiler_Finisher_Feed",
        "if":{"Type": "Broiler Finisher", "Age_Weeks": (4,7)},
        "then":{"Recommend":"Broiler Finishers Mash",
                "DCP": "18-19%",
                "Daily_Feed_g": 80,
                "Advice":"Feed broiler finisher mash for growth.  "}},
#some general rules 
    {
        "name": "R_Layer_Calcium_Warning",
        "priority": 2, 
        "if": {"Type": "Layer", "Age_Weeks": (0, 76)},
        "then": {"Warning": "High calcium damages kidneys"}
    },
    {
        "name":"R_Water_Requirement",
        "if":{"Any": True},
        "then":{"Reminder":"Provide Clean, fresh water at all times. Wash drinkers regularly to avoid diseases"}
    },
    {
        "name": "R_Feed_Hygiene",
        "if":{"Any": True},
        "then":{"Warning":"Avoid damp or moldy feed. Mycotoxins could cause poisoning"}
    },
    {
        "name": "R_Layer_LowProduction",
        "if": {"Type": "Layer", "Age_Weeks": (20, 76), "EggProduction": "<50%"},
        "then": {"Recommend": "Grower Mash", 
            "DCP": "16-18%",
            "Advice":"Reduce feed cost since egg production is low."}
    },
    {
        "name": "R_emergency_filler",
        "if": {"FeedCost": "High"},
        "then": {"Recommend": "Alternative Feed Mix",
            "Advice":"Use maize bran + fishmeal as cheaper substitute."}
},
    {
        "name": "R_Broiler_Sick",
        "if": {"Type": "Broiler Finisher", "Age_Weeks": (4, 6), "Health": "Sick"},
        "then": {"Recommend": "Chick Mash", 
            "DCP": "20-22%",
            "Advice":"Use softer feed to help sick broilers recover."}
}
    ]
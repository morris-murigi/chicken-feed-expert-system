recipes = {
    # Chick Starter (0-8 weeks)
    'Chick Starter': {
        'name': 'Chick and Duck Mash (0-8 weeks)',
        'target_dcp': '18-20% protein',
        'ingredients': {
            'Whole Maize': 31.5,  # ~45% of 70kg bag
            'Wheat Bran': 9.1,    # ~13% of 70kg bag
            'Wheat Pollard': 7.0,  # ~10% of 70kg bag
            'Sunflower or Linseed': 16.8,  # ~24% of 70kg bag
            'Fishmeal (e.g., Omena)': 1.5,  # ~2% of 70kg bag
            'Lime (Calcium Source)': 1.75,  # ~2.5% of 70kg bag
            'Salt': 0.3,          # ~0.4% of 70kg bag
            'Premix Amino Acids': 0.03,     # ~0.04% of 70kg bag
            'Tryptophan': 0.07,   # ~0.1% of 70kg bag
            'Lysine': 0.003,      # ~0.004% of 70kg bag
            'Methionine': 0.01,   # ~0.01% of 70kg bag
            'Threonine': 0.07,    # ~0.1% of 70kg bag
            'Enzymes': 0.05,      # ~0.07% of 70kg bag
            'Coccidiostat': 0.06, # ~0.09% of 70kg bag
            'Toxin Binder': 0.05  # ~0.07% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'Increase protein by 2% with extra soybean meal (e.g., add 1.4kg soybean)',
            'Moderate Egg Production (70-85%)': 'Maintain current protein, ensure calcium (add 0.5kg lime if needed)',
            'High Egg Production (>85%)': 'Boost calcium by 1kg lime, add 0.5kg vitamin premix',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Add 0.1kg antibiotics, 0.2kg vitamin premix, consult vet',
            'High Cost': 'Use premium fishmeal (2kg) and soybean meal (5kg), expect 20% cost increase',
            'Low Cost': 'Substitute fishmeal with sunflower cake (2kg), reduce premix to 0.02kg, save 15%'
        },
        'expense_estimate': '50-60% of production cost, reducible to 40% with local sourcing'
    },
    # Pullets / Growers (8-18 weeks)
    'Pullets / Growers': {
        'name': 'Growers Mash (8-18 weeks)',
        'target_dcp': '16-18% protein',
        'ingredients': {
            'Whole Maize': 40.0,   # ~57% of 70kg bag
            'Maize Germ': 16.7,    # ~24% of 70kg bag
            'Wheat Pollard': 13.3,  # ~19% of 70kg bag
            'Wheat Bran': 10.0,    # ~14% of 70kg bag
            'Cotton Seed Cake': 6.0,  # ~9% of 70kg bag
            'Sunflower Cake': 4.7,  # ~7% of 70kg bag
            'Fishmeal': 3.0,       # ~4% of 70kg bag
            'Lime': 2.0,           # ~3% of 70kg bag
            'Soya Meal': 3.4,      # ~5% of 70kg bag
            'Bone Meal': 0.04,     # ~0.06% of 70kg bag
            'Grower Premix': 0.01, # ~0.01% of 70kg bag
            'Salt': 0.005,         # ~0.007% of 70kg bag
            'Coccidiostat': 0.005, # ~0.007% of 70kg bag
            'Zincbacitrach': 0.005 # ~0.007% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'N/A for growers, focus on growth',
            'Moderate Egg Production (70-85%)': 'N/A for growers',
            'High Egg Production (>85%)': 'N/A for growers',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Add 0.1kg vitamins, reduce feeding density by 10%',
            'High Cost': 'Use premium soya meal (4kg), expect 15% cost rise',
            'Low Cost': 'Increase maize bran (5kg), reduce fishmeal to 2kg, save 20%'
        },
        'expense_estimate': 'Reduce total cost by 30% with local maize and bran'
    },
    # Layer (18+ weeks)
    'Layer': {
        'name': 'Layers Mash (18+ weeks)',
        'target_dcp': '16-18% protein',
        'ingredients': {
            'Whole Maize': 34.0,    # ~49% of 70kg bag
            'Soya': 12.0,           # ~17% of 70kg bag
            'Fishmeal': 8.0,        # ~11% of 70kg bag
            'Maize Bran/Rice Germ/Wheat Bran': 10.0,  # ~14% of 70kg bag
            'Lime': 6.0,            # ~9% of 70kg bag
            'Premix Amino Acids': 0.175,  # ~0.25% of 70kg bag
            'Lysine': 0.07,         # ~0.1% of 70kg bag
            'Methionine': 0.035,    # ~0.05% of 70kg bag
            'Threonine': 0.07,      # ~0.1% of 70kg bag
            'Tryptophan': 0.035,    # ~0.05% of 70kg bag
            'Toxin Binder': 0.05    # ~0.07% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'Increase calcium by 1kg lime, protein by 2% (add 1.5kg soya)',
            'Moderate Egg Production (70-85%)': 'Maintain calcium, add 0.1kg vitamin premix',
            'High Egg Production (>85%)': 'Boost calcium by 1.5kg lime, add 0.2kg premix',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Add 0.15kg antibiotics, 0.3kg vitamin premix, consult vet',
            'High Cost': 'Use premium fishmeal (10kg) and soya (15kg), expect 25% cost increase',
            'Low Cost': 'Substitute fishmeal with sunflower cake (5kg), save 20%'
        },
        'expense_estimate': '80% of production cost, reducible to 50-60% with homemade'
    },
    # Broiler Starter (0-4 weeks)
    'Broiler Starter': {
        'name': 'Broiler Starter Feed (0-4 weeks)',
        'target_dcp': '22-24% protein',
        'ingredients': {
            'Whole Maize': 40.0,    # ~57% of 70kg bag
            'Fishmeal (e.g., Omena)': 12.0,  # ~17% of 70kg bag
            'Soya Bean Meal': 14.0,  # ~20% of 70kg bag
            'Lime': 4.0,            # ~6% of 70kg bag
            'Premix': 0.07,         # ~0.1% of 70kg bag
            'Salt': 0.04,           # ~0.06% of 70kg bag
            'Coccidiostat': 0.005,  # ~0.007% of 70kg bag
            'Zincbacitrach': 0.005  # ~0.007% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'N/A for broilers',
            'Moderate Egg Production (70-85%)': 'N/A for broilers',
            'High Egg Production (>85%)': 'N/A for broilers',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Add 0.1kg medications, isolate birds',
            'High Cost': 'Use premium soya (15kg), expect 20% cost rise',
            'Low Cost': 'Increase maize (45kg), reduce fishmeal to 10kg, save 15%'
        },
        'expense_estimate': 'Reduce cost by 30-40% with local maize'
    },
    # Broiler Grower (4-7 weeks)
    'Broiler Grower': {
        'name': 'Broiler Grower Feed (4-7 weeks)',
        'target_dcp': '20-22% protein',
        'ingredients': {
            'Whole Maize': 10.0,    # ~14% of 70kg bag
            'Maize Germ': 16.7,     # ~24% of 70kg bag
            'Wheat Pollard': 13.3,  # ~19% of 70kg bag
            'Wheat Bran': 10.0,     # ~14% of 70kg bag
            'Cotton Seed Cake': 6.0,  # ~9% of 70kg bag
            'Sunflower Cake': 4.7,  # ~7% of 70kg bag
            'Fishmeal': 3.0,        # ~4% of 70kg bag
            'Lime': 2.0,            # ~3% of 70kg bag
            'Soya Meal': 3.4,       # ~5% of 70kg bag
            'Bone Meal': 0.04,      # ~0.06% of 70kg bag
            'Grower Premix': 0.01,  # ~0.01% of 70kg bag
            'Salt': 0.005,          # ~0.007% of 70kg bag
            'Coccidiostat': 0.005,  # ~0.007% of 70kg bag
            'Zincbacitrach': 0.005  # ~0.007% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'N/A for broilers',
            'Moderate Egg Production (70-85%)': 'N/A for broilers',
            'High Egg Production (>85%)': 'N/A for broilers',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Add 0.1kg vitamins, monitor closely',
            'High Cost': 'Use premium fishmeal (4kg), expect 15% cost rise',
            'Low Cost': 'Substitute with sunflower cake (5kg), save 20%'
        },
        'expense_estimate': 'Major cost reduction with homemade mix'
    },
    # Broiler Finisher (7+ weeks)
    'Broiler Finisher': {
        'name': 'Broiler Finisher Feed (7+ weeks)',
        'target_dcp': '18% protein',
        'ingredients': {
            'Whole Maize': 35.0,    # ~50% of 70kg bag
            'Maize Germ': 15.0,     # ~21% of 70kg bag
            'Wheat Pollard': 10.0,  # ~14% of 70kg bag
            'Soya': 5.0,            # ~7% of 70kg bag
            'Sunflower': 3.0,       # ~4% of 70kg bag
            'Fishmeal': 2.0,        # ~3% of 70kg bag
            'Lime': 0.07,           # ~0.1% of 70kg bag
            'Salt': 0.04,           # ~0.06% of 70kg bag
            'Coccidiostat': 0.005,  # ~0.007% of 70kg bag
            'Zincbacitrach': 0.005  # ~0.007% of 70kg bag
        },
        'units': 'kg per 70kg bag (percentages approximate)',
        'adjustments': {
            'Low Egg Production (<70%)': 'N/A for broilers',
            'Moderate Egg Production (70-85%)': 'N/A for broilers',
            'High Egg Production (>85%)': 'N/A for broilers',
            'Healthy': 'Standard recipe sufficient',
            'Sick': 'Reduce density by 10%, add 0.1kg supplements',
            'High Cost': 'Use premium ingredients (5kg soya), expect 20% rise',
            'Low Cost': 'Increase grain (40kg), save 25%'
        },
        'expense_estimate': 'Save 30% on commercial feeds'
    }
}

rules = [
    # Chick (0-8 weeks)
    {"conditions": {"Type": "Chick", "Age_Weeks": {"operator": "<=", "value": 8}}, "consequence": {"Recommend": "Chick Starter"}},
    # Pullets / Growers (8-18 weeks)
    {"conditions": {"Type": "Pullets / Growers", "Age_Weeks": {"operator": ">", "value": 8, "operator2": "<=", "value2": 18}}, "consequence": {"Recommend": "Pullets / Growers"}},
    # Layer (18+ weeks)
    {"conditions": {"Type": "Layer", "Age_Weeks": {"operator": ">=", "value": 18}}, "consequence": {"Recommend": "Layer"}},
    # Broiler Starter (0-4 weeks)
    {"conditions": {"Type": "Broiler Starter", "Age_Weeks": {"operator": "<=", "value": 4}}, "consequence": {"Recommend": "Broiler Starter"}},
    # Broiler Grower (4-7 weeks)
    {"conditions": {"Type": "Broiler Grower", "Age_Weeks": {"operator": ">", "value": 4, "operator2": "<=", "value2": 7}}, "consequence": {"Recommend": "Broiler Grower"}},
    # Broiler Finisher (7+ weeks)
    {"conditions": {"Type": "Broiler Finisher", "Age_Weeks": {"operator": ">", "value": 7}}, "consequence": {"Recommend": "Broiler Finisher"}},
    # Egg Production Levels
    {"conditions": {"EggProduction": {"operator": "<", "value": "70%"}}, "consequence": {"Warnings": "Low egg production (<70%). Increase protein by 2% (e.g., add 1.4kg soybean meal)."}},
    {"conditions": {"EggProduction": {"operator": ">=", "value": "70%", "operator2": "<=", "value": "85%"}}, "consequence": {"Warnings": "Moderate egg production (70-85%). Maintain current recipe, ensure calcium (add 0.5kg lime if needed)."}},
    {"conditions": {"EggProduction": {"operator": ">", "value": "85%"}}, "consequence": {"Warnings": "High egg production (>85%). Boost calcium by 1.5kg lime, add 0.2kg vitamin premix."}},
    # Health Factors
    {"conditions": {"Health": "Healthy"}, "consequence": {"Warnings": "Healthy birds. Standard recipe sufficient."}},
    {"conditions": {"Health": "Sick"}, "consequence": {"Warnings": "Sick birds. Add 0.15kg antibiotics, 0.3kg vitamin premix, consult vet."}},
    # Expense Levels
    {"conditions": {"FeedCost": "High"}, "consequence": {"Warnings": "High cost selected. Use premium fishmeal (10kg) and soya (15kg), expect 25% cost increase."}},
    {"conditions": {"FeedCost": "Low"}, "consequence": {"Warnings": "Low cost selected. Substitute fishmeal with sunflower cake (5kg), save 20%."}},
    {"conditions": {"FeedCost": ""}, "consequence": {"Warnings": "No cost preference. Use standard recipe."}}
]

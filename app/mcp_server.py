# app/mcp_server.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_models import FeedQuery
from app.inference_engine import apply_rules, get_feed_recipe
from app.knowledge_base import CHICKEN_FRAMES, RECIPE_FRAMES, INGREDIENT_FRAMES

# Create the MCP server
mcp_server = FastMCP("Chicken Feed Expert")

@mcp_server.tool()
def get_feed_recommendation(
    chicken_type: str,
    age_weeks: float,
    egg_production: Optional[str] = None,
    feed_cost: Optional[str] = None,
    health: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get chicken feed recommendation based on type, age, and conditions.
    
    Args:
        chicken_type: Type of chicken (Chick, Grower, Layer, Broiler Starter, Broiler Grower, Broiler Finisher)
        age_weeks: Age of chicken in weeks
        egg_production: Egg production rate (e.g., "<50%" for layers)
        feed_cost: Cost consideration ("High" if cost is a concern)
        health: Health status ("Sick" if chickens are unwell)
    
    Returns:
        Complete feed recommendation with recipe and advice
    """
    try:
        # Create FeedQuery object using your existing data model
        feed_query = FeedQuery(
            Type=chicken_type,
            Age_Weeks=age_weeks,
            EggProduction=egg_production,
            FeedCost=feed_cost,
            Health=health
        )
        
        # Use your existing inference engine
        facts = feed_query.dict()
        recommendations = apply_rules(facts)
        
        # Get recipe using your existing logic
        feed_type = None
        for rec in recommendations:
            if "Recommend" in rec:
                feed_type = rec["Recommend"]
                break
        
        recipe = get_feed_recipe(feed_type) if feed_type else {}
        
        return {
            "facts": facts,
            "recommendations": recommendations,
            "recipe": recipe,
            "success": True
        }
        
    except Exception as e:
        return {
            "error": f"Failed to get recommendation: {str(e)}",
            "success": False
        }

# Fix: Use proper URI format with file:// scheme
@mcp_server.resource("file:///chicken-types/info")
def get_chicken_types() -> str:
    """Get information about available chicken types and their characteristics"""
    info = "Available Chicken Types and Their Characteristics:\n\n"
    
    for chicken_type, details in CHICKEN_FRAMES.items():
        info += f"**{chicken_type}:**\n"
        info += f"  - Age Stage: {details.get('Age_Stage', 'N/A')}\n"
        info += f"  - Primary Goal: {details.get('Primary_Goal', 'N/A')}\n"
        info += f"  - Recommended Feed: {details.get('Recommended_Feed_Type', 'N/A')}\n"
        info += f"  - Protein Requirement: {details.get('Protein_Requirement_DCP_Range', 'N/A')}\n"
        info += f"  - Daily Feed Consumption: {details.get('Daily_Feed_Consumption_g', 'N/A')}g\n\n"
    
    return info

@mcp_server.resource("file:///feed-recipes/all")
def get_all_recipes() -> str:
    """Get all available feed recipes with ingredients and proportions"""
    recipes_info = "Available Feed Recipes (70kg batches):\n\n"
    
    for recipe_name, recipe_details in RECIPE_FRAMES.items():
        recipes_info += f"**{recipe_name}:**\n"
        recipes_info += f"  - Target Type: {recipe_details['Target_Type']}\n"
        recipes_info += f"  - Target Protein (DCP): {recipe_details['Target_DCP']}\n"
        recipes_info += "  - Ingredients:\n"
        
        for ingredient, amount in recipe_details['Ingredients'].items():
            recipes_info += f"    • {ingredient}: {amount}kg\n"
        recipes_info += "\n"
    
    return recipes_info

@mcp_server.resource("file:///ingredients/info")
def get_ingredient_info() -> str:
    """Get information about feed ingredients including nutritional content and prices"""
    ingredient_info = "Feed Ingredients Information:\n\n"
    
    for ingredient, details in INGREDIENT_FRAMES.items():
        ingredient_info += f"**{ingredient}:**\n"
        ingredient_info += f"  - Type: {details['Type']}\n"
        ingredient_info += f"  - Crude Protein: {details['CP%']}%\n"
        ingredient_info += f"  - Price per kg: KES {details['Price_per_kg']}\n"
        ingredient_info += f"  - Quality Control: {details['QC']}\n\n"
    
    return ingredient_info

@mcp_server.tool()
def calculate_feed_cost(recipe_name: str, batch_size_kg: float = 70.0) -> Dict[str, Any]:
    """
    Calculate the total cost of a feed recipe based on current ingredient prices.
    
    Args:
        recipe_name: Name of the recipe (e.g., "70kg Chick Mash")
        batch_size_kg: Size of the batch in kg (default: 70kg)
    
    Returns:
        Cost breakdown and total cost
    """
    try:
        if recipe_name not in RECIPE_FRAMES:
            return {"error": f"Recipe '{recipe_name}' not found", "success": False}
        
        recipe = RECIPE_FRAMES[recipe_name]
        cost_breakdown = {}
        total_cost = 0.0
        scaling_factor = batch_size_kg / 70.0  # Recipes are for 70kg batches
        
        for ingredient, amount_kg in recipe['Ingredients'].items():
            if ingredient in INGREDIENT_FRAMES:
                scaled_amount = amount_kg * scaling_factor
                ingredient_cost = INGREDIENT_FRAMES[ingredient]['Price_per_kg'] * scaled_amount
                cost_breakdown[ingredient] = {
                    "amount_kg": round(scaled_amount, 2),
                    "price_per_kg": INGREDIENT_FRAMES[ingredient]['Price_per_kg'],
                    "total_cost": round(ingredient_cost, 2)
                }
                total_cost += ingredient_cost
        
        return {
            "recipe_name": recipe_name,
            "batch_size_kg": batch_size_kg,
            "cost_breakdown": cost_breakdown,
            "total_cost": round(total_cost, 2),
            "cost_per_kg": round(total_cost / batch_size_kg, 2),
            "success": True
        }
        
    except Exception as e:
        return {"error": f"Failed to calculate cost: {str(e)}", "success": False}

@mcp_server.tool()
def get_feeding_advice(chicken_type: str, specific_concern: Optional[str] = None) -> Dict[str, Any]:
    """
    Get general feeding advice and tips for specific chicken types.
    
    Args:
        chicken_type: Type of chicken
        specific_concern: Specific concern like "low egg production", "sick birds", "cost reduction"
    
    Returns:
        Feeding advice and tips
    """
    try:
        if chicken_type not in CHICKEN_FRAMES:
            return {"error": f"Chicken type '{chicken_type}' not recognized", "success": False}
        
        chicken_info = CHICKEN_FRAMES[chicken_type]
        advice = {
            "chicken_type": chicken_type,
            "basic_advice": {
                "primary_goal": chicken_info.get("Primary_Goal"),
                "recommended_feed": chicken_info.get("Recommended_Feed_Type"),
                "daily_consumption": f"{chicken_info.get('Daily_Feed_Consumption_g')}g per bird",
                "protein_requirement": chicken_info.get("Protein_Requirement_DCP_Range")
            },
            "general_tips": [
                "Provide clean, fresh water at all times",
                "Wash drinkers regularly to avoid diseases", 
                "Avoid damp or moldy feed - mycotoxins can cause poisoning",
                "Store feed in dry, cool conditions"
            ],
            "success": True
        }
        
        # Add specific advice based on concerns
        if specific_concern:
            if specific_concern.lower() in ["low egg production", "poor laying"]:
                advice["specific_advice"] = [
                    "Consider switching to grower mash if egg production is below 50%",
                    "Check for stress factors (overcrowding, temperature, lighting)",
                    "Ensure adequate calcium levels for shell formation"
                ]
            elif specific_concern.lower() in ["sick", "disease", "health"]:
                advice["specific_advice"] = [
                    "Consider softer feed (chick mash) for sick birds",
                    "Isolate sick birds to prevent spread",
                    "Consult a veterinarian for proper diagnosis"
                ]
            elif specific_concern.lower() in ["cost", "expensive", "budget"]:
                advice["specific_advice"] = [
                    "Consider maize bran + fishmeal as cheaper substitute",
                    "Buy ingredients in bulk to reduce costs",
                    "Mix your own feed using local ingredients"
                ]
        
        return advice
        
    except Exception as e:
        return {"error": f"Failed to get advice: {str(e)}", "success": False}

if __name__ == "__main__":
    # Run the MCP server
    mcp_server.run()
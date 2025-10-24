"""
Flask API for sauce recommendation and optimization services.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the parent directory to the path so we can import sauce_maximizer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sauce_maximizer import SauceOptimizer, RecipeAnalyzer, FlavorPredictor

app = Flask(__name__)
CORS(app)

# Initialize core components
optimizer = SauceOptimizer()
analyzer = RecipeAnalyzer()
predictor = FlavorPredictor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "sauce-maximizer-api"})

@app.route('/api/optimize', methods=['POST'])
def optimize_recipe():
    """
    Optimize a sauce recipe based on provided parameters.
    
    Expected JSON payload:
    {
        "base_recipe": {
            "name": "tomato_base",
            "ingredients": {"tomato": 0.6, "garlic": 0.1, "oil": 0.3},
            "target_flavor": {"umami": 0.8, "sweet": 0.3}
        },
        "optimization_goals": {"flavor_score": 1.0, "cost": -0.5}
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'base_recipe' not in data:
            return jsonify({"error": "Missing base_recipe in request"}), 400
            
        # Extract recipe data
        recipe_data = data['base_recipe']
        optimization_goals = data.get('optimization_goals', {"flavor_score": 1.0})
        
        # Perform optimization (placeholder)
        result = {
            "optimized_recipe": recipe_data,  # Would be actual optimization result
            "improvement_score": 0.15,
            "optimization_details": {
                "iterations": 50,
                "convergence": True,
                "flavor_improvement": 0.12
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict_flavor', methods=['POST'])
def predict_flavor():
    """Predict flavor score for a recipe."""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', {})
        
        # Placeholder prediction
        predicted_score = 0.75  # Would use actual ML model
        
        return jsonify({
            "predicted_flavor_score": predicted_score,
            "confidence": 0.85,
            "flavor_breakdown": {
                "umami": 0.7,
                "sweet": 0.3,
                "salty": 0.5,
                "sour": 0.2,
                "spicy": 0.1
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_recipe():
    """Analyze a recipe and provide insights."""
    try:
        data = request.get_json()
        recipe_data = data.get('recipe', {})
        
        # Placeholder analysis
        analysis = {
            "nutritional_score": 0.8,
            "cost_estimate": 3.50,
            "similar_recipes": ["classic_marinara", "garlic_tomato"],
            "suggestions": [
                "Consider adding basil for improved flavor complexity",
                "Reduce salt content by 10% for better balance"
            ]
        }
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
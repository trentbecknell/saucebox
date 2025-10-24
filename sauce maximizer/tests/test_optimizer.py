import pytest
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sauce_maximizer.core.optimizer import SauceOptimizer, Recipe, Ingredient

class TestSauceOptimizer:
    """Test cases for the SauceOptimizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = SauceOptimizer()
        self.sample_recipe = Recipe(
            name="test_sauce",
            ingredients={"tomato": 0.6, "garlic": 0.2, "oil": 0.2},
            target_flavor={"umami": 0.8, "sweet": 0.3},
            constraints={"max_cost": 5.0}
        )
    
    def test_optimizer_initialization(self):
        """Test that optimizer initializes correctly."""
        assert isinstance(self.optimizer, SauceOptimizer)
        assert self.optimizer.ingredients == {}
        assert self.optimizer.optimization_history == []
    
    def test_recipe_creation(self):
        """Test recipe object creation."""
        assert self.sample_recipe.name == "test_sauce"
        assert len(self.sample_recipe.ingredients) == 3
        assert sum(self.sample_recipe.ingredients.values()) == 1.0
    
    def test_flavor_score_prediction(self):
        """Test flavor score prediction method."""
        score = self.optimizer.predict_flavor_score(self.sample_recipe)
        assert isinstance(score, float)
        assert score >= 0.0
    
    def test_ingredient_synergy_analysis(self):
        """Test ingredient synergy analysis."""
        ingredients = ["tomato", "garlic", "basil"]
        synergy = self.optimizer.analyze_ingredient_synergy(ingredients)
        assert isinstance(synergy, dict)
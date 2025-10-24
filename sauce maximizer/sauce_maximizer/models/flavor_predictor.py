"""
Machine learning models for mix quality prediction and enhancement suggestions.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import joblib

class MixPredictor:
    """ML model for predicting mix quality and suggesting improvements."""
    
    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.quality_model = None  # Predicts overall mix quality (0-1)
        self.processing_model = None  # Suggests processing parameters
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def prepare_training_data(self, audio_features_df) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare audio feature data for model training.
        
        Args:
            audio_features_df: DataFrame with audio features and quality ratings
            
        Returns:
            X: Feature matrix (spectral features, balance metrics, etc.)
            y: Target values (quality scores from professional ratings)
        """
        # Extract audio features for training
        feature_columns = [
            'spectral_centroid', 'spectral_rolloff', 'rms_energy', 'dynamic_range',
            'bass_energy', 'mid_energy', 'high_energy', 'stereo_width',
            'loudness_lufs', 'crest_factor', 'frequency_spread'
        ]
        
        X = audio_features_df[feature_columns].values
        y = audio_features_df['professional_rating'].values  # 0-10 scale
        
        # Normalize features
        X = self.scaler.fit_transform(X)
        self.feature_names = feature_columns
        
        return X, y
        
    def train_quality_model(self, X: np.ndarray, y: np.ndarray, 
                           validation_split: float = 0.2) -> Dict[str, float]:
        """
        Train the mix quality prediction model.
        
        Returns:
            Dict with training metrics and feature importance
        """
        if self.model_type == "random_forest":
            self.quality_model = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        elif self.model_type == "gradient_boosting":
            self.quality_model = GradientBoostingRegressor(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=8,
                random_state=42
            )
            
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42
        )
        
        self.quality_model.fit(X_train, y_train)
        self.is_trained = True
        
        # Calculate metrics
        train_score = self.quality_model.score(X_train, y_train)
        val_score = self.quality_model.score(X_val, y_val)
        
        # Predict on validation set for additional metrics
        y_pred = self.quality_model.predict(X_val)
        mae = np.mean(np.abs(y_val - y_pred))
        rmse = np.sqrt(np.mean((y_val - y_pred)**2))
        
        return {
            "train_r2": train_score,
            "validation_r2": val_score,
            "validation_mae": mae,
            "validation_rmse": rmse,
            "feature_importance": self.get_feature_importance()
        }
        
    def predict_mix_quality(self, audio_features: Dict[str, float]) -> Dict[str, float]:
        """
        Predict mix quality and identify areas for improvement.
        
        Args:
            audio_features: Dict of extracted audio features
            
        Returns:
            Dict with quality prediction and improvement suggestions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
            
        # Convert features to array in correct order
        feature_vector = np.array([audio_features.get(name, 0.0) for name in self.feature_names])
        feature_vector = self.scaler.transform(feature_vector.reshape(1, -1))
        
        # Predict overall quality
        quality_score = self.quality_model.predict(feature_vector)[0]
        quality_score = np.clip(quality_score / 10.0, 0.0, 1.0)  # Normalize to 0-1
        
        # Analyze specific areas for improvement
        improvement_areas = self._analyze_improvement_areas(audio_features)
        
        # Get confidence based on feature similarity to training data
        confidence = self._calculate_prediction_confidence(feature_vector)
        
        return {
            "overall_quality": float(quality_score),
            "confidence": float(confidence),
            "improvement_areas": improvement_areas,
            "predicted_rating": float(quality_score * 10),  # 0-10 scale
            "quality_category": self._categorize_quality(quality_score)
        }
        
    def suggest_processing_parameters(self, audio_features: Dict[str, float]) -> Dict[str, any]:
        """
        Suggest specific processing parameters based on mix analysis.
        
        Returns:
            Dict with specific EQ, compression, and other processing suggestions
        """
        suggestions = {
            'eq_adjustments': {},
            'compression': {},
            'stereo_enhancement': {},
            'harmonic_enhancement': {},
            'priority_order': []
        }
        
        # Analyze frequency balance
        bass_energy = audio_features.get('bass_energy', 0)
        mid_energy = audio_features.get('mid_energy', 0) 
        high_energy = audio_features.get('high_energy', 0)
        total_energy = bass_energy + mid_energy + high_energy
        
        if total_energy > 0:
            bass_ratio = bass_energy / total_energy
            high_ratio = high_energy / total_energy
            
            # Bass adjustments
            if bass_ratio < 0.15:
                suggestions['eq_adjustments']['low_shelf'] = {
                    'frequency': 100,
                    'gain_db': min(4.0, (0.15 - bass_ratio) * 20),
                    'q': 0.7
                }
                suggestions['priority_order'].append('bass_boost')
            elif bass_ratio > 0.4:
                suggestions['eq_adjustments']['high_pass'] = {
                    'frequency': 60 + (bass_ratio - 0.4) * 200,
                    'q': 0.8
                }
                suggestions['priority_order'].append('bass_reduction')
                
            # High frequency adjustments
            if high_ratio < 0.08:
                suggestions['eq_adjustments']['high_shelf'] = {
                    'frequency': 8000,
                    'gain_db': min(3.0, (0.08 - high_ratio) * 30),
                    'q': 0.6
                }
                suggestions['priority_order'].append('brightness')
                
        # Dynamic range analysis
        dynamic_range = audio_features.get('dynamic_range', 0)
        rms_energy = audio_features.get('rms_energy', 0)
        
        if dynamic_range > 0.8 and rms_energy > 0.1:
            # Needs compression
            suggestions['compression'] = {
                'threshold_db': -18.0 + (dynamic_range - 0.8) * 20,
                'ratio': 2.5 + min(2.0, (dynamic_range - 0.8) * 5),
                'attack_ms': 15.0,
                'release_ms': 100.0,
                'knee': 2.0
            }
            suggestions['priority_order'].append('compression')
        elif dynamic_range < 0.15:
            # Over-compressed, suggest parallel processing
            suggestions['compression'] = {
                'type': 'parallel',
                'blend': 30.0,
                'threshold_db': -25.0,
                'ratio': 1.5
            }
            suggestions['priority_order'].append('dynamic_restoration')
            
        # Stereo width analysis
        stereo_width = audio_features.get('stereo_width', 0.5)
        if stereo_width < 0.3:
            suggestions['stereo_enhancement'] = {
                'width_multiplier': 1.2 + (0.3 - stereo_width),
                'low_freq_mono': 120,  # Keep bass centered
                'type': 'mid_side'
            }
            suggestions['priority_order'].append('stereo_width')
            
        return suggestions
        
    def train_from_reference_tracks(self, reference_audio_paths: List[str], 
                                  amateur_audio_paths: List[str]) -> Dict[str, float]:
        """
        Train model using reference professional tracks vs amateur mixes.
        
        Args:
            reference_audio_paths: Paths to professional reference tracks
            amateur_audio_paths: Paths to amateur/unpolished mixes
            
        Returns:
            Training metrics
        """
        # This would extract features from audio files and create training data
        # with professional tracks rated highly and amateur tracks rated lower
        
        # Placeholder - in real implementation would:
        # 1. Load and analyze all audio files
        # 2. Extract comprehensive feature sets
        # 3. Assign quality ratings (high for reference, lower for amateur)
        # 4. Train the model
        
        return {"placeholder": True, "message": "Would train on actual audio files"}
        
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from trained model."""
        if not self.is_trained or not hasattr(self.quality_model, 'feature_importances_'):
            return {}
            
        importance_dict = dict(zip(self.feature_names, self.quality_model.feature_importances_))
        
        # Sort by importance
        sorted_importance = dict(sorted(importance_dict.items(), 
                                      key=lambda x: x[1], reverse=True))
        
        return sorted_importance
        
    def save_model(self, filepath: str) -> None:
        """Save trained model to disk."""
        if self.is_trained:
            model_data = {
                'quality_model': self.quality_model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'model_type': self.model_type
            }
            joblib.dump(model_data, filepath)
            
    def load_model(self, filepath: str) -> None:
        """Load trained model from disk."""
        model_data = joblib.load(filepath)
        self.quality_model = model_data['quality_model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.model_type = model_data['model_type']
        self.is_trained = True
        
    def _analyze_improvement_areas(self, features: Dict[str, float]) -> List[str]:
        """Identify specific areas where the mix could be improved."""
        issues = []
        
        # Check frequency balance
        bass_energy = features.get('bass_energy', 0)
        high_energy = features.get('high_energy', 0)
        total_energy = sum([features.get(f'{band}_energy', 0) for band in ['bass', 'mid', 'high']])
        
        if total_energy > 0:
            if bass_energy / total_energy < 0.1:
                issues.append("insufficient_low_end")
            elif bass_energy / total_energy > 0.45:
                issues.append("excessive_bass")
                
            if high_energy / total_energy < 0.05:
                issues.append("lacks_brightness")
                
        # Check dynamics
        dynamic_range = features.get('dynamic_range', 0)
        if dynamic_range < 0.1:
            issues.append("over_compressed")
        elif dynamic_range > 0.9:
            issues.append("needs_compression")
            
        # Check stereo characteristics
        stereo_width = features.get('stereo_width', 0.5)
        if stereo_width < 0.2:
            issues.append("too_narrow")
        elif stereo_width > 0.9:
            issues.append("too_wide")
            
        # Check overall level
        rms_energy = features.get('rms_energy', 0)
        if rms_energy < 0.1:
            issues.append("too_quiet")
        elif rms_energy > 0.8:
            issues.append("too_loud")
            
        return issues
        
    def _calculate_prediction_confidence(self, feature_vector: np.ndarray) -> float:
        """Calculate confidence in prediction based on feature similarity to training data."""
        # Simplified confidence calculation
        # In practice, could use uncertainty quantification methods
        return 0.85  # Placeholder
        
    def _categorize_quality(self, quality_score: float) -> str:
        """Categorize quality score into descriptive labels."""
        if quality_score >= 0.8:
            return "professional"
        elif quality_score >= 0.6:
            return "good"
        elif quality_score >= 0.4:
            return "needs_work"
        else:
            return "requires_major_improvement"
"""
SauceMax - An intelligent audio plugin for mix enhancement.

This package provides tools for analyzing audio mixes and suggesting
optimal processing chains to achieve professional-sounding results.
"""

__version__ = "0.1.0"
__author__ = "SauceMax Team"

# Safe imports with fallbacks
try:
    from .core.analyzer import MixAnalyzer
except ImportError as e:
    print(f"Warning: Could not import MixAnalyzer: {e}")
    MixAnalyzer = None

try:
    from .core.optimizer import AudioProcessor  
except ImportError as e:
    print(f"Warning: Could not import AudioProcessor: {e}")
    AudioProcessor = None

try:
    from .models.flavor_predictor import MixPredictor
except ImportError as e:
    print(f"Warning: Could not import MixPredictor: {e}")
    MixPredictor = None

# Only export what was successfully imported
__all__ = []
if MixAnalyzer is not None:
    __all__.append("MixAnalyzer")
if AudioProcessor is not None:
    __all__.append("AudioProcessor") 
if MixPredictor is not None:
    __all__.append("MixPredictor")
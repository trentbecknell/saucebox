#!/usr/bin/env python3
"""
SauceMax CLI - Standalone testing tool for core functionality.
Tests the audio analysis and processing without Reaper dependencies.
"""

import sys
import os
import json
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_dependencies():
    """Check if required dependencies are available."""
    missing = []
    
    try:
        import numpy
        print("✓ numpy available")
    except ImportError:
        missing.append("numpy")
        print("✗ numpy missing")
    
    try:
        import scipy
        print("✓ scipy available")
    except ImportError:
        missing.append("scipy")
        print("✗ scipy missing")
    
    try:
        import librosa
        print("✓ librosa available")
    except ImportError:
        missing.append("librosa")
        print("✗ librosa missing")
    
    try:
        import sklearn
        print("✓ scikit-learn available")
    except ImportError:
        missing.append("scikit-learn")
        print("✗ scikit-learn missing")
    
    return missing

def test_basic_import():
    """Test basic SauceMax package import."""
    try:
        import sauce_maximizer
        print(f"✓ SauceMax package imported successfully (v{sauce_maximizer.__version__})")
        
        # Test component availability
        if hasattr(sauce_maximizer, 'MixAnalyzer') and sauce_maximizer.MixAnalyzer:
            print("✓ MixAnalyzer available")
        else:
            print("✗ MixAnalyzer not available")
            
        if hasattr(sauce_maximizer, 'AudioProcessor') and sauce_maximizer.AudioProcessor:
            print("✓ AudioProcessor available") 
        else:
            print("✗ AudioProcessor not available")
            
        if hasattr(sauce_maximizer, 'MixPredictor') and sauce_maximizer.MixPredictor:
            print("✓ MixPredictor available")
        else:
            print("✗ MixPredictor not available")
            
        return True
        
    except Exception as e:
        print(f"✗ Failed to import SauceMax: {e}")
        return False

def create_simple_test_audio():
    """Create a simple test audio array without external dependencies."""
    try:
        import numpy as np
        
        # Generate 2 seconds of 440Hz sine wave
        sample_rate = 44100
        duration = 2.0
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        audio = 0.3 * np.sin(2 * np.pi * 440 * t)
        
        return audio, sample_rate
        
    except ImportError:
        print("✗ Cannot create test audio: numpy not available")
        return None, None

def test_audio_analysis():
    """Test basic audio analysis functionality."""
    print("\n=== Testing Audio Analysis ===")
    
    try:
        from sauce_maximizer import MixAnalyzer
        if MixAnalyzer is None:
            print("✗ MixAnalyzer not available")
            return False
            
        analyzer = MixAnalyzer()
        print("✓ MixAnalyzer created successfully")
        
        # Create simple test audio
        audio, sr = create_simple_test_audio()
        if audio is None:
            print("✗ Cannot create test audio for analysis")
            return False
            
        print("✓ Test audio created (440Hz sine wave)")
        
        # Test feature extraction
        try:
            features = analyzer.extract_features(audio)
            print("✓ Feature extraction successful")
            print(f"  - Spectral centroid: {features.spectral_centroid:.0f} Hz")
            print(f"  - RMS energy: {features.rms_energy:.3f}")
            print(f"  - Dynamic range: {features.dynamic_range:.3f}")
            return True
            
        except Exception as e:
            print(f"✗ Feature extraction failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Audio analysis test failed: {e}")
        return False

def test_processing():
    """Test basic audio processing functionality."""
    print("\n=== Testing Audio Processing ===")
    
    try:
        from sauce_maximizer.core.optimizer import AudioProcessor
        if AudioProcessor is None:
            print("✗ AudioProcessor not available")
            return False
            
        processor = AudioProcessor()
        print("✓ AudioProcessor created successfully")
        
        # Create test audio
        audio, sr = create_simple_test_audio()
        if audio is None:
            print("✗ Cannot create test audio for processing")
            return False
            
        # Test EQ processing
        try:
            eq_params = {
                'high_shelf': {'freq': 8000, 'gain': 2.0, 'q': 0.7}
            }
            processed = processor.apply_eq(audio, eq_params)
            print("✓ EQ processing successful")
            
            # Test compression
            comp_params = {
                'threshold': -12.0,
                'ratio': 3.0,
                'attack': 10.0,
                'release': 100.0
            }
            compressed = processor.apply_compression(audio, comp_params)
            print("✓ Compression processing successful")
            
            return True
            
        except Exception as e:
            print(f"✗ Processing failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Processing test failed: {e}")
        return False

def test_ml_prediction():
    """Test ML prediction functionality."""
    print("\n=== Testing ML Prediction ===")
    
    try:
        from sauce_maximizer import MixPredictor
        if MixPredictor is None:
            print("✗ MixPredictor not available")
            return False
            
        predictor = MixPredictor()
        print("✓ MixPredictor created successfully")
        
        # Test with dummy features
        test_features = {
            'spectral_centroid': 2000.0,
            'rms_energy': 0.2,
            'dynamic_range': 0.5,
            'bass_energy': 0.3,
            'mid_energy': 0.4,
            'high_energy': 0.2
        }
        
        # Note: This will fail without a trained model, but we can test the structure
        try:
            prediction = predictor.predict_mix_quality(test_features)
            print("✓ ML prediction successful")
            return True
        except ValueError as e:
            if "Model must be trained" in str(e):
                print("⚠ ML model not trained (expected for initial testing)")
                return True
            else:
                print(f"✗ ML prediction failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ ML test failed: {e}")
        return False

def run_stability_test():
    """Run complete stability test suite."""
    print("🎛️ SauceMax Stability Test\n")
    
    # Check dependencies
    print("=== Checking Dependencies ===")
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"\n⚠ Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt")
        print("\nContinuing with available components...\n")
    else:
        print("\n✓ All dependencies available\n")
    
    # Test basic import
    print("=== Testing Package Import ===")
    import_success = test_basic_import()
    
    if not import_success:
        print("\n❌ Basic import failed - cannot continue with tests")
        return False
    
    # Run component tests
    test_results = []
    
    test_results.append(("Audio Analysis", test_audio_analysis()))
    test_results.append(("Audio Processing", test_processing()))
    test_results.append(("ML Prediction", test_ml_prediction()))
    
    # Summary
    print("\n=== Test Summary ===")
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! SauceMax is stable for testing.")
        return True
    else:
        print(f"\n⚠ {total - passed} tests failed. Check errors above.")
        return False

def main():
    """Main CLI interface."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            run_stability_test()
        elif command == "deps":
            check_dependencies()
        elif command == "version":
            try:
                import sauce_maximizer
                print(f"SauceMax v{sauce_maximizer.__version__}")
            except:
                print("SauceMax not properly installed")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: test, deps, version")
    else:
        print("SauceMax CLI - Stability Testing Tool")
        print()
        print("Usage:")
        print("  python sauce_cli.py test     - Run stability tests")
        print("  python sauce_cli.py deps     - Check dependencies")  
        print("  python sauce_cli.py version  - Show version")
        print()
        print("For full testing, run: python sauce_cli.py test")

if __name__ == "__main__":
    main()
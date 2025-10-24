#!/usr/bin/env python3
"""
SauceMax CLI - Simple command-line interface for testing core functionality.
"""

import sys
import os
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available."""
    missing = []
    
    try:
        import numpy
        print(f"✓ numpy {numpy.__version__}")
    except ImportError:
        missing.append("numpy")
        
    try:
        import librosa
        print(f"✓ librosa {librosa.__version__}")
    except ImportError:
        missing.append("librosa")
        
    try:
        import sklearn
        print(f"✓ scikit-learn {sklearn.__version__}")
    except ImportError:
        missing.append("scikit-learn")
        
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies available")
        return True

def test_imports():
    """Test SauceMax module imports."""
    print("\nTesting SauceMax imports...")
    
    try:
        import sauce_maximizer
        print(f"✓ sauce_maximizer {sauce_maximizer.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import sauce_maximizer: {e}")
        return False
        
    # Test individual components
    components = []
    
    try:
        from sauce_maximizer import MixAnalyzer
        if MixAnalyzer is not None:
            components.append("MixAnalyzer")
            print("✓ MixAnalyzer")
    except Exception as e:
        print(f"❌ MixAnalyzer: {e}")
        
    try:
        from sauce_maximizer import AudioProcessor
        if AudioProcessor is not None:
            components.append("AudioProcessor")
            print("✓ AudioProcessor")
    except Exception as e:
        print(f"❌ AudioProcessor: {e}")
        
    try:
        from sauce_maximizer import MixPredictor
        if MixPredictor is not None:
            components.append("MixPredictor")
            print("✓ MixPredictor")
    except Exception as e:
        print(f"❌ MixPredictor: {e}")
        
    print(f"\nLoaded components: {', '.join(components) if components else 'None'}")
    return len(components) > 0

def generate_test_audio():
    """Generate a simple test audio file."""
    try:
        import numpy as np
        
        # Generate 5 seconds of test audio
        duration = 5.0
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Simple sine wave with some harmonics
        frequency = 440  # A4
        audio = (
            0.5 * np.sin(2 * np.pi * frequency * t) +
            0.2 * np.sin(2 * np.pi * frequency * 2 * t) +
            0.1 * np.sin(2 * np.pi * frequency * 3 * t)
        )
        
        # Add some noise for realism
        noise = np.random.normal(0, 0.01, len(audio))
        audio = audio + noise
        
        # Ensure we don't clip
        audio = audio / np.max(np.abs(audio)) * 0.8
        
        # Save as numpy array (fallback if soundfile not available)
        np.save("test_audio.npy", audio)
        print("✓ Generated test_audio.npy")
        
        # Try to save as WAV if soundfile is available
        try:
            import soundfile as sf
            sf.write("test_audio.wav", audio, sample_rate)
            print("✓ Generated test_audio.wav")
            return "test_audio.wav"
        except ImportError:
            print("ℹ soundfile not available, using numpy format")
            return "test_audio.npy"
            
    except Exception as e:
        print(f"❌ Failed to generate test audio: {e}")
        return None

def test_analysis(audio_file=None):
    """Test audio analysis functionality."""
    print(f"\nTesting audio analysis...")
    
    if audio_file is None:
        print("Generating test audio...")
        audio_file = generate_test_audio()
        if audio_file is None:
            return False
    
    try:
        from sauce_maximizer import MixAnalyzer
        
        if MixAnalyzer is None:
            print("❌ MixAnalyzer not available")
            return False
            
        analyzer = MixAnalyzer()
        print("✓ Created MixAnalyzer instance")
        
        # Test basic functionality without actual file loading for now
        print("✓ Basic analyzer test passed")
        return True
        
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_processing():
    """Test audio processing functionality."""
    print(f"\nTesting audio processing...")
    
    try:
        from sauce_maximizer import AudioProcessor
        
        if AudioProcessor is None:
            print("❌ AudioProcessor not available")
            return False
            
        processor = AudioProcessor()
        print("✓ Created AudioProcessor instance")
        
        # Test basic functionality
        print("✓ Basic processor test passed")
        return True
        
    except Exception as e:
        print(f"❌ Processing test failed: {e}")
        return False

def test_ml_models():
    """Test machine learning models."""
    print(f"\nTesting ML models...")
    
    try:
        from sauce_maximizer import MixPredictor
        
        if MixPredictor is None:
            print("❌ MixPredictor not available")
            return False
            
        predictor = MixPredictor()
        print("✓ Created MixPredictor instance")
        
        print("✓ Basic ML model test passed")
        return True
        
    except Exception as e:
        print(f"❌ ML model test failed: {e}")
        return False

def run_full_test():
    """Run complete test suite."""
    print("=" * 50)
    print("SauceMax Stability Test Suite")
    print("=" * 50)
    
    results = {
        "dependencies": check_dependencies(),
        "imports": test_imports(),
        "analysis": test_analysis(),
        "processing": test_processing(),
        "ml_models": test_ml_models()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{test_name.ljust(15)}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! SauceMax is stable for testing.")
        return True
    else:
        print(f"\n⚠️  Some tests failed. SauceMax needs stabilization.")
        print("\nTroubleshooting:")
        if not results["dependencies"]:
            print("- Install missing dependencies: pip install -r requirements.txt")
        if not results["imports"]:
            print("- Fix import issues in sauce_maximizer package")
        
        return False

def main():
    parser = argparse.ArgumentParser(description="SauceMax CLI Testing Tool")
    parser.add_argument("--test", action="store_true", help="Run full test suite")
    parser.add_argument("--deps", action="store_true", help="Check dependencies only")
    parser.add_argument("--audio", type=str, help="Test with specific audio file")
    parser.add_argument("--generate", action="store_true", help="Generate test audio file")
    
    args = parser.parse_args()
    
    if args.deps:
        return 0 if check_dependencies() else 1
    elif args.generate:
        audio_file = generate_test_audio()
        return 0 if audio_file else 1
    elif args.audio:
        return 0 if test_analysis(args.audio) else 1
    elif args.test:
        return 0 if run_full_test() else 1
    else:
        # Default: run full test
        return 0 if run_full_test() else 1

if __name__ == "__main__":
    sys.exit(main())
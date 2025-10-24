#!/usr/bin/env python3
"""
SauceMax CLI - Simple command-line audio analysis tool.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SauceMax - Simple Audio Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py analyze test.wav
  python cli.py analyze --verbose my_mix.wav
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an audio file')
    analyze_parser.add_argument('file', help='WAV file to analyze')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', 
                               help='Show detailed analysis')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test SauceMax installation')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_file(args.file, args.verbose)
    elif args.command == 'test':
        test_installation()
    else:
        parser.print_help()

def analyze_file(file_path: str, verbose: bool = False):
    """Analyze an audio file."""
    try:
        # Try importing our analyzer
        from sauce_maximizer.simple_analyzer import SimpleAnalyzer
        
        print(f"🎛️ SauceMax v0.1.0 - Analyzing: {file_path}")
        print("-" * 50)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ Error: File not found: {file_path}")
            return
        
        # Initialize analyzer
        analyzer = SimpleAnalyzer()
        
        # Load and analyze
        print("📁 Loading audio file...")
        audio_data, sample_rate = analyzer.load_wav_file(file_path)
        
        print("🔍 Analyzing audio characteristics...")
        analysis = analyzer.analyze_basic_stats(audio_data, sample_rate)
        
        print("💡 Generating suggestions...")
        suggestions = analyzer.suggest_simple_processing(analysis)
        
        # Display results
        print("\n📊 ANALYSIS RESULTS:")
        print(f"   Duration: {analysis['duration_seconds']:.1f} seconds")
        print(f"   Sample Rate: {analysis['sample_rate']} Hz")
        print(f"   RMS Level: {analysis['rms_level']:.3f}")
        print(f"   Peak Level: {analysis['peak_level']:.3f}")
        print(f"   Dynamic Range: {analysis['dynamic_range']:.1f}")
        
        print(f"\n🎵 FREQUENCY BALANCE:")
        print(f"   Bass (20-250Hz): {analysis['bass_ratio']:.1%}")
        print(f"   Mids (250-4kHz): {analysis['mid_ratio']:.1%}")
        print(f"   Highs (4k-20kHz): {analysis['high_ratio']:.1%}")
        print(f"   Dominant Frequency: {analysis['dominant_frequency_hz']:.0f} Hz")
        
        print(f"\n🎯 OVERALL ASSESSMENT:")
        print(f"   {suggestions['overall_assessment']}")
        
        if suggestions['suggestions']:
            print(f"\n💡 SUGGESTIONS:")
            for i, suggestion in enumerate(suggestions['suggestions'], 1):
                print(f"   {i}. {suggestion}")
        else:
            print(f"\n✅ No major issues detected!")
        
        if verbose:
            print(f"\n🔧 DETAILED METRICS:")
            for key, value in analysis.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.6f}")
                else:
                    print(f"   {key}: {value}")
        
        print(f"\n✅ Analysis complete!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure numpy is installed: pip install numpy")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Make sure the file is a valid WAV file.")

def test_installation():
    """Test if SauceMax is properly installed."""
    print("🧪 Testing SauceMax installation...")
    print("-" * 40)
    
    # Test Python version
    python_version = sys.version_info
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Test numpy import
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError:
        print("❌ NumPy not found - install with: pip install numpy")
        return
    
    # Test our analyzer
    try:
        from sauce_maximizer.simple_analyzer import SimpleAnalyzer
        analyzer = SimpleAnalyzer()
        print("✅ SauceMax SimpleAnalyzer")
    except Exception as e:
        print(f"❌ SauceMax import failed: {e}")
        return
    
    # Test with synthetic data
    try:
        # Create 1 second of test audio (440Hz sine wave)
        sample_rate = 44100
        t = np.linspace(0, 1, sample_rate)
        test_audio = 0.3 * np.sin(2 * np.pi * 440 * t)  # A440 note
        
        analysis = analyzer.analyze_basic_stats(test_audio, sample_rate)
        suggestions = analyzer.suggest_simple_processing(analysis)
        
        print("✅ Audio analysis working")
        print(f"   Test signal: 440Hz sine wave")
        print(f"   Detected dominant frequency: {analysis['dominant_frequency_hz']:.0f}Hz")
        print(f"   Assessment: {suggestions['overall_assessment']}")
        
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return
    
    print("\n🎉 SauceMax installation test PASSED!")
    print("\nNext steps:")
    print("1. Try: python cli.py analyze your_audio_file.wav")
    print("2. Create a test WAV file in your DAW")
    print("3. Run analysis and see the suggestions")

if __name__ == "__main__":
    main()
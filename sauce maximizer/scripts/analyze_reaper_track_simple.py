#!/usr/bin/env python3
"""
Simplified Reaper integration script for SauceMax audio analysis.
This version uses only basic dependencies (numpy + standard library).
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from sauce_maximizer.simple_analyzer import SimpleAnalyzer
except ImportError as e:
    print(f"Error: Could not import SimpleAnalyzer: {e}")
    sys.exit(1)

def analyze_reaper_track(audio_file: str, track_name: str) -> dict:
    """
    Analyze audio track exported from Reaper.
    
    Args:
        audio_file: Path to exported audio WAV file
        track_name: Name of the track for reference
        
    Returns:
        Analysis results dict
    """
    if not os.path.exists(audio_file):
        return {"error": f"Audio file not found: {audio_file}"}
    
    try:
        # Initialize simple analyzer
        analyzer = SimpleAnalyzer()
        
        # Load audio
        audio_data, sample_rate = analyzer.load_wav_file(audio_file)
        
        # Analyze
        analysis = analyzer.analyze_basic_stats(audio_data, sample_rate)
        
        # Get suggestions
        suggestions = analyzer.suggest_simple_processing(analysis)
        
        # Determine recommended chain based on analysis
        recommended_chain = determine_processing_chain(analysis)
        
        # Format results
        results = {
            "track_name": track_name,
            "analysis": analysis,
            "suggestions": suggestions,
            "recommended_chain": recommended_chain,
            "processing_details": get_processing_details(analysis, recommended_chain)
        }
        
        return results
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def determine_processing_chain(analysis: dict) -> str:
    """
    Determine the best processing chain based on analysis.
    
    Args:
        analysis: Results from analyze_basic_stats
        
    Returns:
        Chain type: "balanced", "bright", or "warm"
    """
    bass_ratio = analysis.get('bass_ratio', 0)
    high_ratio = analysis.get('high_ratio', 0)
    dynamic_range = analysis.get('dynamic_range', 0)
    rms_level = analysis.get('rms_level', 0)
    
    # Decision logic for chain selection
    if high_ratio < 0.05:
        return "bright"  # Needs brightness
    elif bass_ratio > 0.5:
        return "balanced"  # Too much bass, needs balance
    elif dynamic_range < 2.0:
        return "warm"  # Over-compressed, add warmth
    elif rms_level < 0.1 and bass_ratio < 0.15:
        return "bright"  # Quiet and lacking bass/highs
    else:
        return "balanced"  # General balance is best default

def get_processing_details(analysis: dict, chain_type: str) -> dict:
    """
    Get specific processing parameters based on chain type and analysis.
    
    Args:
        analysis: Analysis results
        chain_type: Type of processing chain
        
    Returns:
        Dict with processing parameters
    """
    details = {}
    
    if chain_type == "bright":
        details["eq"] = {
            "high_shelf": {
                "freq": 8000,
                "gain": 3.0 if analysis.get('high_ratio', 0) < 0.03 else 2.0
            },
            "high_pass": {
                "freq": 80
            }
        }
        details["compression"] = {
            "threshold": -18,
            "ratio": 2.5,
            "attack": 15,
            "release": 100
        }
        
    elif chain_type == "warm":
        details["eq"] = {
            "low_shelf": {
                "freq": 100,
                "gain": 2.0
            }
        }
        details["compression"] = {
            "threshold": -15,
            "ratio": 2.0,
            "attack": 20,
            "release": 150
        }
        details["saturation"] = {
            "drive": 0.15
        }
        
    else:  # balanced
        details["eq"] = {
            "high_shelf": {
                "freq": 8000,
                "gain": 1.5
            },
            "low_shelf": {
                "freq": 100,
                "gain": 1.0
            }
        }
        details["compression"] = {
            "threshold": -12,
            "ratio": 3.0,
            "attack": 10,
            "release": 100
        }
    
    return details

def generate_reaper_readable_output(results: dict, output_file: str):
    """
    Generate output file that Reaper can read and display.
    
    Args:
        results: Analysis results dict
        output_file: Path to write output text file
    """
    if "error" in results:
        output_text = f"SauceMax Analysis Error:\n{results['error']}"
    else:
        track_name = results.get('track_name', 'Unknown Track')
        analysis = results.get('analysis', {})
        suggestions = results.get('suggestions', {})
        recommended_chain = results.get('recommended_chain', 'balanced')
        processing = results.get('processing_details', {})
        
        output_text = f"""SauceMax Analysis Results: {track_name}
{'=' * 60}

OVERALL ASSESSMENT:
{suggestions.get('overall_assessment', 'Analysis complete')}

Recommended Processing Chain: {recommended_chain.upper()}

AUDIO CHARACTERISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Duration:       {analysis.get('duration_seconds', 0):.2f} seconds
Sample Rate:    {analysis.get('sample_rate', 0)} Hz
RMS Level:      {analysis.get('rms_level', 0):.3f}
Peak Level:     {analysis.get('peak_level', 0):.3f}
Dynamic Range:  {analysis.get('dynamic_range', 0):.2f}

FREQUENCY BALANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bass (20-250Hz):     {analysis.get('bass_ratio', 0):.1%}
Mids (250-4kHz):     {analysis.get('mid_ratio', 0):.1%}
Highs (4k-20kHz):    {analysis.get('high_ratio', 0):.1%}
Dominant Frequency:  {analysis.get('dominant_frequency_hz', 0):.0f} Hz
"""

        # Add suggestions
        suggestion_list = suggestions.get('suggestions', [])
        if suggestion_list:
            output_text += "\nSUGGESTIONS:\n"
            output_text += "━" * 60 + "\n"
            for i, suggestion in enumerate(suggestion_list, 1):
                output_text += f"{i}. {suggestion}\n"
        
        # Add processing details
        if processing:
            output_text += "\nRECOMMENDED PROCESSING SETTINGS:\n"
            output_text += "━" * 60 + "\n"
            
            # EQ settings
            if "eq" in processing:
                output_text += "\nEQ Adjustments:\n"
                eq = processing["eq"]
                if "high_shelf" in eq:
                    output_text += f"  • High Shelf: +{eq['high_shelf']['gain']:.1f}dB @ {eq['high_shelf']['freq']}Hz\n"
                if "low_shelf" in eq:
                    output_text += f"  • Low Shelf: +{eq['low_shelf']['gain']:.1f}dB @ {eq['low_shelf']['freq']}Hz\n"
                if "high_pass" in eq:
                    output_text += f"  • High Pass: {eq['high_pass']['freq']}Hz\n"
            
            # Compression settings
            if "compression" in processing:
                comp = processing["compression"]
                output_text += "\nCompression:\n"
                output_text += f"  • Threshold: {comp['threshold']:.1f}dB\n"
                output_text += f"  • Ratio: {comp['ratio']:.1f}:1\n"
                output_text += f"  • Attack: {comp['attack']:.1f}ms\n"
                output_text += f"  • Release: {comp['release']:.1f}ms\n"
            
            # Saturation
            if "saturation" in processing:
                sat = processing["saturation"]
                output_text += "\nSaturation:\n"
                output_text += f"  • Drive: {sat['drive']:.2f}\n"

        output_text += f"""

NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Apply '{recommended_chain}' processing chain in SauceMax
2. A/B test with original mix
3. Adjust parameters to taste based on above suggestions
4. Consider using a reference track for comparison

Generated by SauceMax v0.1.0
"""
    
    # Write to file for Reaper to read
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(output_text)
        print(f"Results written to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)

def main():
    """Main function for command-line usage from Reaper."""
    if len(sys.argv) < 3:
        print("Usage: python analyze_reaper_track_simple.py <audio_file> <track_name>")
        print("\nExample:")
        print("  python analyze_reaper_track_simple.py my_track.wav \"Lead Vocal\"")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    track_name = sys.argv[2]
    
    print(f"🎛️ SauceMax Reaper Integration")
    print(f"Analyzing: {track_name}")
    print("-" * 60)
    
    # Perform analysis
    results = analyze_reaper_track(audio_file, track_name)
    
    # Generate output for Reaper
    script_dir = Path(__file__).parent
    output_file = script_dir / "analysis_results.txt"
    generate_reaper_readable_output(results, str(output_file))
    
    # Also output JSON for programmatic access
    json_output = script_dir / "analysis_results.json"
    try:
        # Convert numpy types to Python types for JSON serialization
        def convert_types(obj):
            if hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        json_data = convert_types(results)
        with open(json_output, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"JSON data written to: {json_output}")
    except Exception as e:
        print(f"Warning: Could not write JSON output: {e}", file=sys.stderr)
    
    # Print status for Reaper script
    if "error" in results:
        print(f"\n❌ ANALYSIS_ERROR: {results['error']}")
        sys.exit(1)
    else:
        print(f"\n✅ ANALYSIS_SUCCESS: Recommended chain - {results['recommended_chain']}")
        print(f"\nTo view detailed results, check: {output_file}")
        sys.exit(0)

if __name__ == "__main__":
    main()

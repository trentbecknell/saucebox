#!/usr/bin/env python3
"""
Reaper integration script for SauceMax audio analysis.
Analyzes audio exported from Reaper and generates processing suggestions.
"""

import sys
import os
import json
import numpy as np
import librosa
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from sauce_maximizer.core.analyzer import MixAnalyzer, AudioFeatures
from sauce_maximizer.models.flavor_predictor import MixPredictor

def analyze_reaper_track(audio_file: str, track_name: str) -> dict:
    """
    Analyze audio track exported from Reaper.
    
    Args:
        audio_file: Path to exported audio file
        track_name: Name of the track for reference
        
    Returns:
        Analysis results dict
    """
    if not os.path.exists(audio_file):
        return {"error": f"Audio file not found: {audio_file}"}
    
    try:
        # Initialize analyzer
        analyzer = MixAnalyzer()
        
        # Load audio
        audio, sr = analyzer.load_audio(audio_file)
        
        # Extract features
        features = analyzer.extract_features(audio)
        
        # Analyze mix balance
        balance_scores = analyzer.analyze_mix_balance(audio)
        
        # Generate processing suggestions
        processing_suggestions = analyzer.suggest_processing_chain(features)
        
        # Format results for Reaper display
        results = {
            "track_name": track_name,
            "analysis": {
                "spectral_centroid": features.spectral_centroid,
                "rms_energy": features.rms_energy,
                "dynamic_range": features.dynamic_range,
                "stereo_width": features.stereo_width,
                "frequency_balance": features.frequency_balance
            },
            "balance_scores": balance_scores,
            "processing_suggestions": processing_suggestions,
            "recommended_chain": determine_best_chain(features, balance_scores),
            "confidence": processing_suggestions.get('overall_confidence', 0.5)
        }
        
        return results
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def determine_best_chain(features: AudioFeatures, balance_scores: dict) -> str:
    """Determine the best processing chain based on analysis."""
    
    # Calculate overall balance score
    avg_balance = np.mean(list(balance_scores.values()))
    
    # Check frequency characteristics
    freq_balance = features.frequency_balance
    total_energy = sum(freq_balance.values()) if freq_balance else 1
    
    if total_energy > 0:
        bass_ratio = freq_balance.get('bass', 0) / total_energy
        high_ratio = freq_balance.get('highs', 0) / total_energy
        
        # Decision logic for chain selection
        if high_ratio < 0.05:
            return "bright"  # Needs brightness
        elif bass_ratio > 0.4:
            return "balanced"  # Too much bass, needs balance
        elif features.dynamic_range < 0.2:
            return "warm"  # Over-compressed, add warmth
        elif avg_balance < 0.6:
            return "balanced"  # General balance issues
        else:
            return "warm"  # Default to warm enhancement
    
    return "balanced"

def generate_reaper_readable_output(results: dict, output_file: str):
    """Generate output file that Reaper can read and display."""
    
    if "error" in results:
        output_text = f"SauceMax Analysis Error:\n{results['error']}"
    else:
        track_name = results.get('track_name', 'Unknown Track')
        analysis = results.get('analysis', {})
        suggestions = results.get('processing_suggestions', {})
        recommended_chain = results.get('recommended_chain', 'balanced')
        confidence = results.get('confidence', 0.5)
        
        output_text = f"""SauceMax Analysis Results: {track_name}

OVERALL ASSESSMENT:
Recommended Processing: {recommended_chain.upper()}
Confidence: {confidence:.1%}

FREQUENCY ANALYSIS:
Spectral Centroid: {analysis.get('spectral_centroid', 0):.0f} Hz
RMS Energy: {analysis.get('rms_energy', 0):.3f}
Dynamic Range: {analysis.get('dynamic_range', 0):.3f}
Stereo Width: {analysis.get('stereo_width', 0):.2f}

PROCESSING SUGGESTIONS:"""

        # Add EQ suggestions
        eq_suggestions = suggestions.get('eq', {})
        if eq_suggestions:
            output_text += "\n\nEQ ADJUSTMENTS:"
            for eq_type, params in eq_suggestions.items():
                if eq_type == 'high_shelf':
                    output_text += f"\n• High Shelf: +{params.get('gain', 0):.1f}dB @ {params.get('freq', 8000)}Hz"
                elif eq_type == 'low_shelf':
                    output_text += f"\n• Low Shelf: +{params.get('gain', 0):.1f}dB @ {params.get('freq', 100)}Hz"
                elif eq_type == 'high_pass':
                    output_text += f"\n• High Pass: {params.get('freq', 80)}Hz"

        # Add compression suggestions
        comp_suggestions = suggestions.get('compression', {})
        if comp_suggestions:
            output_text += "\n\nCOMPRESSION:"
            output_text += f"\n• Threshold: {comp_suggestions.get('threshold', -12):.1f}dB"
            output_text += f"\n• Ratio: {comp_suggestions.get('ratio', 3):.1f}:1"
            output_text += f"\n• Attack: {comp_suggestions.get('attack', 10):.1f}ms"
            output_text += f"\n• Release: {comp_suggestions.get('release', 100):.1f}ms"

        # Add next steps
        output_text += f"""

NEXT STEPS:
1. Apply '{recommended_chain}' processing chain in SauceMax
2. A/B test with original mix
3. Adjust parameters to taste
4. Consider reference track comparison

Generated by SauceMax v0.1.0"""
    
    # Write to file for Reaper to read
    try:
        with open(output_file, 'w') as f:
            f.write(output_text)
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    """Main function for command-line usage from Reaper."""
    if len(sys.argv) < 3:
        print("Usage: python analyze_reaper_track.py <audio_file> <track_name>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    track_name = sys.argv[2]
    
    # Perform analysis
    results = analyze_reaper_track(audio_file, track_name)
    
    # Generate output for Reaper
    script_dir = Path(__file__).parent
    output_file = script_dir / "analysis_results.txt"
    generate_reaper_readable_output(results, str(output_file))
    
    # Also output JSON for programmatic access
    json_output = script_dir / "analysis_results.json"
    try:
        with open(json_output, 'w') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error writing JSON output: {e}")
    
    # Print status for Reaper script
    if "error" in results:
        print(f"ANALYSIS_ERROR: {results['error']}")
        sys.exit(1)
    else:
        print(f"ANALYSIS_SUCCESS: {results['recommended_chain']}")
        sys.exit(0)

if __name__ == "__main__":
    main()
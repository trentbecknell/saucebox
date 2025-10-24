#!/usr/bin/env python3
"""
Generate test audio files for SauceMax testing.
"""

import numpy as np
import os
from pathlib import Path

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False
    print("Warning: soundfile not available, using basic numpy save")

def create_test_fixtures():
    """Create basic test audio files."""
    
    # Create fixtures directory
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)
    
    sample_rate = 44100
    duration = 5.0  # 5 seconds
    samples = int(sample_rate * duration)
    
    # Generate test signals
    t = np.linspace(0, duration, samples, False)
    
    # 1. Pure sine wave (440Hz - A4)
    sine_wave = 0.3 * np.sin(2 * np.pi * 440 * t)
    
    # 2. Mixed frequencies (bass + mid + high)
    mixed_signal = (
        0.2 * np.sin(2 * np.pi * 100 * t) +   # Bass
        0.2 * np.sin(2 * np.pi * 1000 * t) +  # Mid
        0.1 * np.sin(2 * np.pi * 5000 * t)    # High
    )
    
    # 3. White noise (for testing dynamic range)
    white_noise = 0.1 * np.random.normal(0, 1, samples)
    
    # 4. Simulated "poor mix" (unbalanced frequencies)
    poor_mix = (
        0.8 * np.sin(2 * np.pi * 80 * t) +    # Too much bass
        0.05 * np.sin(2 * np.pi * 2000 * t) +  # Not enough mids
        0.01 * np.sin(2 * np.pi * 8000 * t)    # Almost no highs
    )
    
    # 5. Simulated "good mix" (balanced)
    good_mix = (
        0.25 * np.sin(2 * np.pi * 100 * t) +   # Balanced bass
        0.3 * np.sin(2 * np.pi * 1500 * t) +   # Good mids
        0.15 * np.sin(2 * np.pi * 7000 * t)    # Appropriate highs
    )
    
    test_files = {
        "test_sine.wav": sine_wave,
        "test_mixed.wav": mixed_signal,
        "test_noise.wav": white_noise,
        "test_poor_mix.wav": poor_mix,
        "test_good_mix.wav": good_mix
    }
    
    # Save test files
    for filename, audio_data in test_files.items():
        file_path = fixtures_dir / filename
        
        if HAS_SOUNDFILE:
            # Use soundfile for proper WAV format
            sf.write(str(file_path), audio_data, sample_rate)
        else:
            # Fallback to numpy save (for basic testing)
            np.save(str(file_path.with_suffix('.npy')), audio_data)
        
        print(f"Created: {file_path}")
    
    # Create a simple metadata file
    metadata = {
        "sample_rate": sample_rate,
        "duration": duration,
        "files": list(test_files.keys()),
        "descriptions": {
            "test_sine.wav": "Pure 440Hz sine wave",
            "test_mixed.wav": "Mixed bass/mid/high frequencies", 
            "test_noise.wav": "White noise for dynamic range testing",
            "test_poor_mix.wav": "Unbalanced mix (too much bass)",
            "test_good_mix.wav": "Well-balanced mix"
        }
    }
    
    import json
    with open(fixtures_dir / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nTest fixtures created in: {fixtures_dir}")
    print("Files:", list(test_files.keys()))
    return fixtures_dir

if __name__ == "__main__":
    create_test_fixtures()
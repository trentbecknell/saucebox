# SauceMax Usage Examples

This document provides practical examples for using SauceMax locally and with Reaper.

## Table of Contents

- [Installation Examples](#installation-examples)
- [CLI Usage Examples](#cli-usage-examples)
- [Reaper Integration Examples](#reaper-integration-examples)
- [Custom Script Examples](#custom-script-examples)

## Installation Examples

### Quick Install and Test

```bash
# Navigate to the sauce maximizer directory
cd "sauce maximizer"

# One-command install and test
make quick-start
```

Output:
```
Installing SauceMax...
✅ Installation complete!
Testing SauceMax installation...
✅ Python 3.12.3
✅ NumPy 2.3.4
✅ SauceMax SimpleAnalyzer
✅ Audio analysis working
🎉 SauceMax installation test PASSED!
```

### Manual Install

```bash
# Using pip
pip3 install -e .

# Verify
python3 -c "import sauce_maximizer; print('✓ Installed')"
```

### Install with Virtual Environment

```bash
# Create virtual environment
python3 -m venv saucemax_env

# Activate it
source saucemax_env/bin/activate

# Install
pip install -e .

# Test
python3 cli.py test
```

## CLI Usage Examples

### Example 1: Basic Analysis

```bash
# Analyze an audio file
python3 cli.py analyze my_mix.wav
```

Output:
```
🎛️ SauceMax v0.1.0 - Analyzing: my_mix.wav
--------------------------------------------------
📁 Loading audio file...
🔍 Analyzing audio characteristics...
💡 Generating suggestions...

📊 ANALYSIS RESULTS:
   Duration: 3.5 seconds
   Sample Rate: 44100 Hz
   RMS Level: 0.245
   Peak Level: 0.812
   Dynamic Range: 3.3

🎵 FREQUENCY BALANCE:
   Bass (20-250Hz): 18.5%
   Mids (250-4kHz): 68.2%
   Highs (4k-20kHz): 13.3%
   Dominant Frequency: 523 Hz

🎯 OVERALL ASSESSMENT:
   Mix sounds well-balanced

✅ No major issues detected!
```

### Example 2: Verbose Analysis

```bash
# Get detailed metrics
python3 cli.py analyze --verbose my_mix.wav
```

Additional output includes:
```
🔧 DETAILED METRICS:
   duration_seconds: 3.500000
   rms_level: 0.245123
   peak_level: 0.812456
   dynamic_range: 3.314567
   dominant_frequency_hz: 523.251159
   bass_ratio: 0.185234
   mid_ratio: 0.682451
   high_ratio: 0.132315
   sample_rate: 44100
   total_samples: 154350
```

### Example 3: Batch Processing

```bash
# Analyze multiple files
for file in *.wav; do
    echo "Analyzing: $file"
    python3 cli.py analyze "$file" > "analysis_${file%.wav}.txt"
done
```

### Example 4: Using Makefile Commands

```bash
# Test with generated sample
make test-analyze

# Output:
# Generating test audio...
# Created test_sample.wav
# Analyzing test audio...
# [... analysis results ...]
```

## Reaper Integration Examples

### Example 1: Test Reaper Integration

```bash
# Test with generated audio
make test-reaper
```

Output:
```
Testing Reaper integration...
Generating sample audio for test...
Running Reaper analysis script...
🎛️ SauceMax Reaper Integration
Analyzing: Test Track
------------------------------------------------------------
Results written to: scripts/analysis_results.txt
✅ ANALYSIS_SUCCESS: Recommended chain - balanced
```

### Example 2: Analyze Exported Track

```bash
# After exporting a track from Reaper
make test-reaper AUDIO_FILE=~/Music/my_track_export.wav
```

Or directly:
```bash
python3 scripts/analyze_reaper_track_simple.py ~/Music/my_track_export.wav "Lead Vocal"
```

Output files:
- `scripts/analysis_results.txt` - Human-readable report
- `scripts/analysis_results.json` - Machine-readable data

### Example 3: View Reaper Analysis Results

```bash
# After running analysis
cat scripts/analysis_results.txt
```

Output:
```
SauceMax Analysis Results: Lead Vocal
============================================================

OVERALL ASSESSMENT:
Mix has minor issues that could be improved

Recommended Processing Chain: BRIGHT

AUDIO CHARACTERISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Duration:       4.20 seconds
Sample Rate:    48000 Hz
RMS Level:      0.156
Peak Level:     0.723
Dynamic Range:  4.63

FREQUENCY BALANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bass (20-250Hz):     12.3%
Mids (250-4kHz):     82.1%
Highs (4k-20kHz):    5.6%
Dominant Frequency:  892 Hz

SUGGESTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Limited high frequencies - consider brightness enhancement

RECOMMENDED PROCESSING SETTINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EQ Adjustments:
  • High Shelf: +3.0dB @ 8000Hz
  • High Pass: 80Hz

Compression:
  • Threshold: -18.0dB
  • Ratio: 2.5:1
  • Attack: 15.0ms
  • Release: 100.0ms

NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Apply 'bright' processing chain in SauceMax
2. A/B test with original mix
3. Adjust parameters to taste based on above suggestions
4. Consider using a reference track for comparison

Generated by SauceMax v0.1.0
```

### Example 4: Using in Reaper (Manual Steps)

1. **Export track from Reaper:**
   - Select track
   - File → Render (Ctrl/Cmd+Alt+R)
   - Save as WAV

2. **Run analysis:**
   ```bash
   python3 scripts/analyze_reaper_track_simple.py exported_track.wav "My Track"
   ```

3. **Review results:**
   ```bash
   cat scripts/analysis_results.txt
   ```

4. **Apply in Reaper:**
   - Add ReaEQ: FX → ReaEQ
   - Add ReaComp: FX → ReaComp
   - Configure based on suggestions

## Custom Script Examples

### Example 1: Basic Analysis Script

```python
#!/usr/bin/env python3
from sauce_maximizer.simple_analyzer import SimpleAnalyzer

# Initialize
analyzer = SimpleAnalyzer()

# Load and analyze
audio, sr = analyzer.load_wav_file("my_track.wav")
results = analyzer.analyze_basic_stats(audio, sr)
suggestions = analyzer.suggest_simple_processing(results)

# Print results
print(f"RMS Level: {results['rms_level']:.3f}")
print(f"Peak Level: {results['peak_level']:.3f}")
print(f"Bass: {results['bass_ratio']:.1%}")
print(f"Assessment: {suggestions['overall_assessment']}")
```

### Example 2: Batch Analysis Script

```python
#!/usr/bin/env python3
import os
import json
from pathlib import Path
from sauce_maximizer.simple_analyzer import SimpleAnalyzer

def analyze_directory(directory):
    """Analyze all WAV files in a directory."""
    analyzer = SimpleAnalyzer()
    results = []
    
    for wav_file in Path(directory).glob("*.wav"):
        print(f"Analyzing: {wav_file.name}")
        
        try:
            audio, sr = analyzer.load_wav_file(str(wav_file))
            analysis = analyzer.analyze_basic_stats(audio, sr)
            suggestions = analyzer.suggest_simple_processing(analysis)
            
            results.append({
                "file": wav_file.name,
                "rms_level": float(analysis['rms_level']),
                "peak_level": float(analysis['peak_level']),
                "bass_ratio": float(analysis['bass_ratio']),
                "assessment": suggestions['overall_assessment']
            })
        except Exception as e:
            print(f"Error analyzing {wav_file.name}: {e}")
    
    # Save results
    with open("batch_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalyzed {len(results)} files")
    print("Results saved to: batch_analysis.json")

if __name__ == "__main__":
    analyze_directory(".")
```

### Example 3: Compare Multiple Mixes

```python
#!/usr/bin/env python3
from sauce_maximizer.simple_analyzer import SimpleAnalyzer
import sys

def compare_mixes(file1, file2):
    """Compare two audio files."""
    analyzer = SimpleAnalyzer()
    
    # Analyze both files
    audio1, sr1 = analyzer.load_wav_file(file1)
    results1 = analyzer.analyze_basic_stats(audio1, sr1)
    
    audio2, sr2 = analyzer.load_wav_file(file2)
    results2 = analyzer.analyze_basic_stats(audio2, sr2)
    
    # Compare
    print(f"Comparison: {file1} vs {file2}")
    print("=" * 60)
    print(f"{'Metric':<20} {'File 1':<15} {'File 2':<15} {'Diff':<10}")
    print("-" * 60)
    
    metrics = ['rms_level', 'peak_level', 'bass_ratio', 'mid_ratio', 'high_ratio']
    for metric in metrics:
        val1 = results1[metric]
        val2 = results2[metric]
        diff = val2 - val1
        print(f"{metric:<20} {val1:>14.3f} {val2:>14.3f} {diff:>+9.3f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_mixes.py file1.wav file2.wav")
        sys.exit(1)
    compare_mixes(sys.argv[1], sys.argv[2])
```

### Example 4: Monitor Audio Levels

```python
#!/usr/bin/env python3
import time
from pathlib import Path
from sauce_maximizer.simple_analyzer import SimpleAnalyzer

def monitor_file(wav_file, interval=5):
    """Monitor audio file for level changes."""
    analyzer = SimpleAnalyzer()
    last_mtime = 0
    
    print(f"Monitoring: {wav_file}")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            # Check if file was modified
            mtime = Path(wav_file).stat().st_mtime
            
            if mtime > last_mtime:
                audio, sr = analyzer.load_wav_file(wav_file)
                results = analyzer.analyze_basic_stats(audio, sr)
                
                print(f"[{time.strftime('%H:%M:%S')}] "
                      f"RMS: {results['rms_level']:.3f}, "
                      f"Peak: {results['peak_level']:.3f}, "
                      f"Bass: {results['bass_ratio']:.1%}")
                
                last_mtime = mtime
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python monitor.py audio_file.wav")
        sys.exit(1)
    monitor_file(sys.argv[1])
```

## Integration Examples

### Example 1: Use in CI/CD Pipeline

```yaml
# .github/workflows/audio-test.yml
name: Audio Analysis Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install SauceMax
        run: |
          cd "sauce maximizer"
          pip install -e .
      - name: Run tests
        run: |
          cd "sauce maximizer"
          make test
          make test-analyze
```

### Example 2: Web Service Integration

```python
from flask import Flask, request, jsonify
from sauce_maximizer.simple_analyzer import SimpleAnalyzer
import tempfile
import os

app = Flask(__name__)
analyzer = SimpleAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """Web endpoint for audio analysis."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio_file = request.files['audio']
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Analyze
        audio, sr = analyzer.load_wav_file(tmp_path)
        results = analyzer.analyze_basic_stats(audio, sr)
        suggestions = analyzer.suggest_simple_processing(results)
        
        return jsonify({
            "analysis": {
                "rms_level": float(results['rms_level']),
                "peak_level": float(results['peak_level']),
                "frequency_balance": {
                    "bass": float(results['bass_ratio']),
                    "mid": float(results['mid_ratio']),
                    "high": float(results['high_ratio'])
                }
            },
            "suggestions": suggestions['suggestions'],
            "assessment": suggestions['overall_assessment']
        })
    finally:
        os.unlink(tmp_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Troubleshooting Examples

### Example 1: Check Installation

```bash
# Verify Python version
python3 --version

# Check if package is importable
python3 -c "import sauce_maximizer; print('✓ OK')"

# Run installation test
python3 cli.py test
```

### Example 2: Debug Analysis Failure

```python
#!/usr/bin/env python3
import sys
from sauce_maximizer.simple_analyzer import SimpleAnalyzer

def debug_analyze(wav_file):
    """Debug audio analysis issues."""
    print(f"Debugging: {wav_file}")
    
    try:
        analyzer = SimpleAnalyzer()
        print("✓ Analyzer initialized")
        
        audio, sr = analyzer.load_wav_file(wav_file)
        print(f"✓ Loaded: {len(audio)} samples at {sr}Hz")
        
        results = analyzer.analyze_basic_stats(audio, sr)
        print(f"✓ Analysis complete")
        print(f"  RMS: {results['rms_level']:.3f}")
        print(f"  Peak: {results['peak_level']:.3f}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug.py audio.wav")
        sys.exit(1)
    debug_analyze(sys.argv[1])
```

## Additional Resources

- [README_LOCAL_DEV.md](README_LOCAL_DEV.md) - Complete development guide
- [README.md](README.md) - Main project documentation
- Python Wave Module: https://docs.python.org/3/library/wave.html
- NumPy Documentation: https://numpy.org/doc/
- Reaper ReaScript: https://www.reaper.fm/sdk/reascript/reascript.php

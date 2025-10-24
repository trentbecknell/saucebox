# SauceMax 🎛️

**Simple Audio Analysis Tool** - Analyze your mixes and get basic enhancement suggestions.

> **Note**: This is a minimal, stable version (v0.1.0) focused on core functionality that actually works.

## What It Does

SauceMax analyzes WAV files and provides:
- **Basic audio statistics** (RMS, peak, dynamic range)
- **Frequency balance analysis** (bass/mid/high ratios)
- **Simple processing suggestions** based on common mix issues
- **Command-line interface** for easy testing

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/trentbecknell/saucemax.git
cd saucemax

# Install dependencies (just numpy)
pip install numpy

# Test the installation
python cli.py test
```

### Analyze Your Audio

```bash
# Basic analysis
python cli.py analyze your_mix.wav

# Detailed analysis with verbose output
python cli.py analyze --verbose your_track.wav
```

### Example Output

```
🎛️ SauceMax v0.1.0 - Analyzing: test.wav
--------------------------------------------------
📁 Loading audio file...
🔍 Analyzing audio characteristics...
💡 Generating suggestions...

📊 ANALYSIS RESULTS:
   Duration: 30.0 seconds
   Sample Rate: 44100 Hz
   RMS Level: 0.245
   Peak Level: 0.987
   Dynamic Range: 4.0

🎵 FREQUENCY BALANCE:
   Bass (20-250Hz): 28.5%
   Mids (250-4kHz): 52.3%
   Highs (4k-20kHz): 19.2%
   Dominant Frequency: 440 Hz

🎯 OVERALL ASSESSMENT:
   Mix has minor issues that could be improved

💡 SUGGESTIONS:
   1. Limited high frequencies - consider brightness enhancement
   2. Consider adding dynamics with gentle compression

✅ Analysis complete!
```

## What's Working

✅ **WAV file loading** using Python's built-in `wave` module  
✅ **Basic audio analysis** with numpy-based FFT  
✅ **Frequency band analysis** (bass, mids, highs)  
✅ **Simple suggestion engine** based on common mix issues  
✅ **Command-line interface** with clear output  
✅ **Installation testing** to verify everything works  

## What's Not Yet Implemented

❌ Reaper integration (complex, needs more testing)  
❌ Machine learning models (requires training data)  
❌ Advanced DSP processing (needs more dependencies)  
❌ Real-time analysis (performance optimization needed)  
❌ GUI interface (focus on CLI stability first)  

## Requirements

- **Python 3.7+**
- **NumPy** (only dependency)
- **WAV files** for analysis

## File Support

- ✅ **WAV files** (16-bit, 24-bit, mono/stereo)
- ❌ MP3, FLAC, etc. (not yet supported)

## Testing

Create a test WAV file in your DAW and run:

```bash
python cli.py test
python cli.py analyze your_test_file.wav
```

## Development Philosophy

This version prioritizes **stability over features**. Every feature that's included actually works. As we validate the core functionality, we'll gradually add more advanced features.

## Next Steps

1. **Test with your audio files** and report issues
2. **Validate the analysis results** against manual inspection  
3. **Suggest improvements** for the suggestion engine
4. **Help us prioritize** which features to add next

## Contributing

Found a bug? Have a suggestion? Please:

1. Test with the current stable version
2. Create an issue with your WAV file specs and error details
3. Include the exact command you ran and the output

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**This is real, working software** - not vaporware. Try it now! 🎵
# SauceMax Troubleshooting Guide

This guide helps solve common issues when installing and using SauceMax.

## Installation Issues

### Python Dependencies

**Problem**: `pip install -r requirements.txt` fails
```
ERROR: Could not build wheels for librosa
```

**Solutions**:
1. **Update pip and setuptools**:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Install system dependencies** (Linux):
   ```bash
   sudo apt-get install libsndfile1-dev ffmpeg
   ```

3. **Use conda instead** (recommended for complex audio dependencies):
   ```bash
   conda install -c conda-forge librosa scikit-learn numpy pandas
   ```

**Problem**: `ModuleNotFoundError: No module named 'sauce_maximizer'`

**Solution**: Install in development mode:
```bash
cd saucemax
pip install -e .
```

### Reaper Integration

**Problem**: SauceMax.lua not appearing in Reaper Scripts menu

**Solutions**:
1. **Check installation path**:
   - macOS: `~/Library/Application Support/REAPER/Scripts/`
   - Windows: `%APPDATA%\REAPER\Scripts\`
   - Linux: `~/.config/REAPER/Scripts/`

2. **Refresh Reaper scripts**:
   - Restart Reaper
   - Or go to `Actions → Load ReaScript...` and browse to the file

**Problem**: "Python not found" error in Reaper

**Solutions**:
1. **Update Python path in SauceMax.lua**:
   ```lua
   local PYTHON_EXECUTABLE = "/usr/local/bin/python3"  -- Your Python path
   ```

2. **Check Python installation**:
   ```bash
   which python3
   python3 --version
   ```

3. **Install Python in system PATH** (Windows):
   - Reinstall Python with "Add to PATH" option checked

## Audio Analysis Issues

**Problem**: "Audio file not found" error

**Solutions**:
1. **Check file permissions**:
   ```bash
   chmod 644 your_audio_file.wav
   ```

2. **Supported formats**: WAV, AIFF, MP3, FLAC
   - Convert unsupported formats: `ffmpeg -i input.m4a output.wav`

3. **File path issues**: Avoid spaces and special characters in filenames

**Problem**: Analysis returns poor results or crashes

**Solutions**:
1. **Check audio quality**:
   - Minimum: 44.1kHz, 16-bit
   - Avoid corrupted or very short files (<5 seconds)

2. **Memory issues with large files**:
   - Trim to 30-60 seconds for analysis
   - Use: `ffmpeg -i input.wav -t 60 output_trimmed.wav`

3. **Silence or low-level audio**:
   - Ensure audio has sufficient level (RMS > -40dB)
   - Check for muted tracks in Reaper

## Processing Issues

**Problem**: Processing chains don't sound good

**Solutions**:
1. **Check mix before processing**:
   - Ensure no clipping or distortion
   - Balance levels between instruments first

2. **Adjust confidence threshold**:
   - SauceMax works best with confidence >60%
   - Low confidence suggests problematic source audio

3. **A/B test results**:
   - Use Reaper's bypass to compare before/after
   - Trust your ears over automated suggestions

**Problem**: "No processing needed" message

**Solutions**:
1. **Your mix might already be good!**
   - Professional mixes may need minimal processing
   - This is actually a positive result

2. **Check analysis settings**:
   - Ensure analyzing the correct track/bus
   - Check for phase cancellation or mono compatibility issues

## Performance Issues

**Problem**: Analysis is very slow

**Solutions**:
1. **Reduce audio length**:
   ```bash
   # Analyze first 30 seconds only
   ffmpeg -i input.wav -t 30 analysis_clip.wav
   ```

2. **Close other applications**:
   - Audio analysis is CPU intensive
   - Close unnecessary background processes

3. **Check system requirements**:
   - Minimum: 8GB RAM, multi-core CPU
   - SSD recommended for large audio files

**Problem**: Reaper freezes during analysis

**Solutions**:
1. **Run analysis externally first**:
   ```bash
   python scripts/analyze_reaper_track.py test.wav "Test Track"
   ```

2. **Update Reaper**:
   - Ensure Reaper 6.70+ for best ReaScript compatibility

3. **Increase buffer sizes**:
   - In Reaper: Options → Audio → Device → Buffer size

## Common Error Messages

### `ImportError: librosa requires scipy`
```bash
pip install scipy>=1.7.0
```

### `RuntimeError: No audio backend is available`
```bash
# Install audio backend
pip install soundfile  # Recommended
# OR
pip install audioread
```

### `PermissionError: [Errno 13] Permission denied`
```bash
# Fix file permissions
chmod +x install.sh
sudo chown -R $USER:$USER saucemax/
```

### `SSL Certificate Error` (macOS)
```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

## Getting Help

### Before Reporting Issues

1. **Check system compatibility**:
   - Python 3.8+
   - Supported OS version
   - Sufficient disk space (>1GB)

2. **Try minimal test**:
   ```bash
   python -c "import sauce_maximizer; print('Import successful')"
   python -c "import librosa; print('Librosa working')"
   ```

3. **Collect system info**:
   ```bash
   python --version
   pip list | grep -E "(librosa|numpy|scikit)"
   uname -a  # Linux/macOS
   ```

### Reporting Bugs

Include this information:
- SauceMax version
- Operating system and version
- Python version
- Reaper version (if applicable)
- Complete error message
- Steps to reproduce
- Audio file specifications

### Community Support

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and tips
- **Audio Forums**: Production techniques and best practices

## Advanced Troubleshooting

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Analysis

Test components individually:
```bash
# Test audio loading
python -c "from sauce_maximizer import MixAnalyzer; a=MixAnalyzer(); print(a.load_audio('test.wav'))"

# Test feature extraction
python -c "from sauce_maximizer import MixAnalyzer; a=MixAnalyzer(); audio,sr=a.load_audio('test.wav'); print(a.extract_features(audio))"
```

### Reset Configuration

Remove cached data:
```bash
rm -rf ~/.saucemax/cache/
rm -rf ~/.saucemax/models/
```

### Reinstall from Scratch

Complete clean installation:
```bash
pip uninstall sauce-maximizer
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install sauce-maximizer
```

Still having issues? Check our [GitHub Issues](https://github.com/yourusername/saucemax/issues) or create a new issue with the information above.
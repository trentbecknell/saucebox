# SauceMax - Local Development & Testing Guide

This guide will help you build and test SauceMax locally, including integration with Reaper.

## Quick Start

The fastest way to get started with local development:

```bash
cd "sauce maximizer"
make quick-start
```

This will:
1. Install SauceMax and dependencies
2. Run installation tests
3. Test audio analysis with a sample file

## Prerequisites

- **Python 3.8+** (tested with Python 3.12)
- **pip** (Python package manager)
- **make** (for running build commands)
- **Reaper DAW** (optional, for testing Reaper integration)

### Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/trentbecknell/saucebox.git
   cd saucebox/"sauce maximizer"
   ```

2. **Install SauceMax**:
   ```bash
   make install
   ```

   Or manually:
   ```bash
   pip3 install -e .
   ```

3. **Verify installation**:
   ```bash
   make test
   ```

## Usage

### Command Reference

Run `make help` to see all available commands:

```
make help              # Show all commands
make install           # Install SauceMax package
make test              # Test installation
make test-analyze      # Test audio analysis
make test-reaper       # Test Reaper integration
make clean             # Clean build artifacts
```

### Testing Audio Analysis

#### Test with generated sample:
```bash
make test-analyze
```

#### Test with your own audio file:
```bash
python3 cli.py analyze path/to/your/audio.wav
```

#### Interactive CLI:
```bash
python3 cli.py
```

Available CLI commands:
- `test` - Test installation and dependencies
- `analyze <file>` - Analyze an audio file
- `analyze --verbose <file>` - Show detailed analysis

### Testing Reaper Integration

#### Test with generated sample:
```bash
make test-reaper
```

#### Test with your own audio:
```bash
make test-reaper AUDIO_FILE=path/to/your/audio.wav
```

#### Or run the script directly:
```bash
python3 scripts/analyze_reaper_track_simple.py your_audio.wav "Track Name"
```

This will generate two files:
- `scripts/analysis_results.txt` - Human-readable analysis results
- `scripts/analysis_results.json` - Machine-readable JSON data

## Reaper Integration Setup

To use SauceMax directly in Reaper:

### Method 1: Automated Installation (Recommended)

```bash
./install.sh
```

This will:
- Install SauceMax Python package
- Detect your Reaper installation
- Copy the integration scripts
- Set up the Lua ReaScript

### Method 2: Manual Installation

1. **Install Python package** (if not already done):
   ```bash
   cd "sauce maximizer"
   pip3 install -e .
   ```

2. **Copy Lua script to Reaper**:
   ```bash
   # macOS/Linux
   cp reaper/SauceMax.lua "$HOME/Library/Application Support/REAPER/Scripts/"
   
   # Or find your Reaper scripts folder:
   # Reaper → Options → Show REAPER resource path in Explorer/Finder
   ```

3. **Update Python path in SauceMax.lua**:
   Edit `SauceMax.lua` and set the correct path to your Python installation:
   ```lua
   local PYTHON_EXECUTABLE = "python3"  -- or full path: "/usr/local/bin/python3"
   local SAUCEMAX_PATH = "/path/to/saucebox/sauce maximizer/"
   ```

4. **Load in Reaper**:
   - Open Reaper
   - Actions → Load ReaScript...
   - Select `SauceMax.lua`

### Using SauceMax in Reaper

1. Select a track in Reaper (or master track)
2. Run the SauceMax script (via Actions menu or toolbar button)
3. Choose an analysis option:
   - **Quick Sauce** - Analyze and apply suggested processing
   - **Analyze Mix** - Just analyze without applying effects
   - **Apply Chains** - Apply specific processing chains (Balanced/Bright/Warm)

The script will:
- Export your track temporarily
- Analyze the audio
- Show analysis results
- Optionally apply suggested FX chains

## Development Workflow

### 1. Make Changes

Edit code in `sauce_maximizer/`, `cli.py`, or other files.

### 2. Test Your Changes

```bash
# Quick test
make test

# Test audio analysis
make test-analyze

# Test Reaper integration
make test-reaper
```

### 3. Clean Build Artifacts

```bash
make clean
```

### 4. Optional: Run Linting/Formatting

```bash
# Install dev dependencies first
make install-dev

# Run linting
make lint

# Format code
make format
```

## Project Structure

```
sauce maximizer/
├── cli.py                          # Command-line interface
├── Makefile                        # Build and test commands
├── setup.py                        # Package setup
├── pyproject.toml                  # Package configuration
├── requirements.txt                # Python dependencies
│
├── sauce_maximizer/                # Main package
│   ├── __init__.py
│   ├── simple_analyzer.py          # Basic audio analysis (no heavy deps)
│   ├── core/
│   │   ├── analyzer.py            # Advanced analysis (requires librosa)
│   │   └── optimizer.py           # Processing optimization
│   └── models/
│       └── flavor_predictor.py    # ML-based predictions
│
├── scripts/
│   ├── analyze_reaper_track_simple.py  # Reaper integration (lightweight)
│   └── analyze_reaper_track.py         # Reaper integration (full features)
│
├── reaper/
│   ├── SauceMax.lua               # Reaper ReaScript
│   └── SauceMax_Minimal.lua       # Minimal version
│
└── tests/
    ├── test_optimizer.py          # Unit tests
    └── generate_test_audio.py     # Test data generator
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'sauce_maximizer'"

Run:
```bash
make install
```

### "librosa not available" warning

This is normal! The basic analyzer works without librosa. For full features:
```bash
pip3 install librosa soundfile
```

### Reaper can't find Python

Edit the `SauceMax.lua` file and set the full path:
```lua
local PYTHON_EXECUTABLE = "/usr/local/bin/python3"  -- or your python path
```

Find your Python path with:
```bash
which python3
```

### Permission denied when running scripts

Make scripts executable:
```bash
chmod +x scripts/*.py
chmod +x install.sh
```

## Testing Checklist

Before submitting changes, verify:

- [ ] `make test` passes
- [ ] `make test-analyze` works with sample audio
- [ ] `make test-reaper` generates correct analysis
- [ ] CLI commands work: `python3 cli.py test` and `python3 cli.py analyze`
- [ ] No build artifacts in git (run `make clean`)
- [ ] Code follows existing style

## Advanced Features

### Using with Virtual Environment

```bash
# Create virtual environment
python3 -m venv saucemax_env

# Activate it
source saucemax_env/bin/activate  # macOS/Linux
# or: saucemax_env\Scripts\activate  # Windows

# Install
pip install -e .

# Deactivate when done
deactivate
```

### Running Tests with pytest

```bash
make install-dev
make test-pytest
```

### Custom Analysis Scripts

Create your own analysis script:

```python
from sauce_maximizer.simple_analyzer import SimpleAnalyzer

analyzer = SimpleAnalyzer()
audio, sr = analyzer.load_wav_file("my_track.wav")
results = analyzer.analyze_basic_stats(audio, sr)
suggestions = analyzer.suggest_simple_processing(results)

print(f"RMS Level: {results['rms_level']}")
print(f"Suggestions: {suggestions['suggestions']}")
```

## Contributing

1. Make your changes
2. Test locally: `make quick-start`
3. Clean up: `make clean`
4. Commit and push

## Resources

- [Reaper API Documentation](https://www.reaper.fm/sdk/reascript/reascript.php)
- [Python Wave Module](https://docs.python.org/3/library/wave.html)
- [NumPy Documentation](https://numpy.org/doc/)

## Support

For issues or questions:
1. Check this README
2. Run `make test` to verify installation
3. Check the GitHub issues page
4. Review the Reaper integration logs

## License

See LICENSE file in the repository root.

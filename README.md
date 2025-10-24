# SauceBox

Audio analysis and mix enhancement tools, including SauceMax integration for Reaper.

## Quick Start

For local development and testing:

```bash
cd "sauce maximizer"
make quick-start
```

Or use the test script:

```bash
cd "sauce maximizer"
./test_local.sh
```

## Documentation

- **[Local Development Guide](sauce%20maximizer/README_LOCAL_DEV.md)** - Complete guide for building and testing locally
- **[SauceMax README](sauce%20maximizer/README.md)** - Main project documentation

## What's Inside

- **SauceMax** - Intelligent audio plugin and analysis tool for Reaper DAW
- **CLI Tools** - Command-line audio analysis utilities
- **Python Package** - Audio analysis library with simple and advanced modes

## Features

- 🎛️ **Audio Analysis** - Analyze frequency balance, dynamics, and mix characteristics
- 🎵 **Smart Suggestions** - Get processing recommendations (EQ, compression, etc.)
- 🔧 **Reaper Integration** - Direct integration with Reaper DAW via Lua scripts
- 📊 **Detailed Reports** - Human-readable and JSON output formats
- 🚀 **Easy Setup** - One-command installation and testing

## Requirements

- Python 3.8+
- NumPy (automatically installed)
- Reaper DAW (optional, for DAW integration)

## Installation

```bash
cd "sauce maximizer"
pip3 install -e .
```

## Usage

### Command Line

```bash
# Test installation
python3 cli.py test

# Analyze an audio file
python3 cli.py analyze your_audio.wav

# Run with Makefile
make test-analyze
make test-reaper
```

### Reaper Integration

See the [Local Development Guide](sauce%20maximizer/README_LOCAL_DEV.md#reaper-integration-setup) for detailed Reaper setup instructions.

## Development

```bash
cd "sauce maximizer"

# Install
make install

# Run tests
make test

# Clean build artifacts
make clean

# See all commands
make help
```

## License

MIT
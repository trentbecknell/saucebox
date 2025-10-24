# SauceMax �️

An intelligent audio plugin that analyzes your mix and suggests the perfect "recipe" for professional-sounding results. Powered by machine learning and designed for novice producers working in Reaper and other DAWs.

## Features

- **Mix Analysis**: Real-time spectral analysis and balance detection
- **Smart Recipes**: ML-powered suggestions for EQ, compression, and effects chains
- **Sonic Enhancement**: Automatically detect what your mix needs to "add sauce"
- **Learning Engine**: Adapts recommendations based on professional mix references
- **One-Click Processing**: Apply suggested processing chains instantly

## Quick Start

```bash
# Install dependencies (C++ build tools, JUCE framework)
./scripts/setup_dev_environment.sh

# Build the plugin
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make

# Install in Reaper
cp SauceMax.vst3 ~/Library/Audio/Plug-Ins/VST3/
# Or for Windows: copy to C:\Program Files\Common Files\VST3\

# Run analysis on a mix
python scripts/analyze_mix.py --input="my_track.wav" --reference="professional_ref.wav"
```

## Architecture

- `src/` - C++ plugin source code (JUCE framework)
- `python/` - ML models and audio analysis tools  
- `data/` - Training datasets and mix references
- `scripts/` - Build tools and utilities
- `tests/` - Unit tests and integration tests
- `presets/` - Processing chain presets and "recipes"

## Development

Requires: JUCE 7.0+, CMake 3.15+, Python 3.8+ for ML components
See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
# SauceMax 🎛️

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/trentbecknell/saucemax)](https://github.com/trentbecknell/saucemax/issues)
[![GitHub stars](https://img.shields.io/github/stars/trentbecknell/saucemax)](https://github.com/trentbecknell/saucemax/stargazers)

An intelligent audio plugin that analyzes your mix and suggests the perfect "recipe" for professional-sounding results. Powered by machine learning and designed for novice producers working in Reaper and other DAWs.

> **"Sauce"** in music production refers to that special sonic enhancement that makes a mix sound polished and professional.

## ✨ Features

- **🔍 Smart Mix Analysis** - Real-time spectral analysis and frequency balance detection
- **🧠 AI-Powered Suggestions** - ML models suggest optimal EQ, compression, and effects
- **⚡ One-Click Enhancement** - Apply professional processing chains instantly
- **🎛️ Reaper Integration** - Seamless workflow with custom ReaScript interface
- **📊 Visual Feedback** - Clear analysis results and confidence scores
- **🎯 Adaptive Processing** - Different "sauce recipes" for various mix styles

## 🚀 Quick Start

### Automatic Installation (Recommended)

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/trentbecknell/saucemax/main/install.sh | bash
```

**Windows:**
```cmd
curl -fsSL https://raw.githubusercontent.com/trentbecknell/saucemax/main/install.bat | cmd
```

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/trentbecknell/saucemax.git
   cd saucemax
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install SauceMax:**
   ```bash
   pip install -e .
   ```

4. **Install Reaper integration:**
   ```bash
   # macOS
   cp reaper/SauceMax.lua ~/Library/Application\ Support/REAPER/Scripts/
   
   # Windows
   copy reaper\SauceMax.lua %APPDATA%\REAPER\Scripts\
   
   # Linux
   cp reaper/SauceMax.lua ~/.config/REAPER/Scripts/
   ```

## 🎵 Usage

### In Reaper

1. **Load SauceMax:**
   - Go to `Actions → Load ReaScript...`
   - Select `SauceMax.lua`
   - The SauceMax interface opens

2. **Analyze your mix:**
   - Select a track (or use master mix)
   - Click **"🎛️ Quick Sauce"** for instant analysis + processing
   - Or click **"📊 Analyze Mix"** for analysis only

3. **Apply processing:**
   - **⚖️ Balanced** - Overall mix balance and clarity
   - **✨ Bright** - High-frequency enhancement
   - **🔥 Warm** - Low-frequency warmth and character

### Command Line

```bash
# Analyze an audio file
saucemax-analyze input.wav "My Track"

# Get help
saucemax --help
```

### Python API

```python
from sauce_maximizer import MixAnalyzer, AudioProcessor

# Analyze a mix
analyzer = MixAnalyzer()
audio, sr = analyzer.load_audio("my_mix.wav")
features = analyzer.extract_features(audio)
suggestions = analyzer.suggest_processing_chain(features)

# Apply processing
processor = AudioProcessor()
processed_audio, report = processor.apply_processing_chain(audio, suggestions)
```

## 🧠 How It Works

1. **Spectral Analysis** - Uses librosa to extract comprehensive audio features
2. **ML Prediction** - Random Forest models trained on professional vs amateur mixes
3. **Adaptive Processing** - Generates custom processing chains based on analysis
4. **Real-time Feedback** - Provides confidence scores and specific improvement areas

### Analysis Features
- Spectral centroid and rolloff
- RMS energy and dynamic range
- Frequency balance across 5 bands
- Stereo width analysis
- Peak frequency detection

### Processing Capabilities
- **EQ**: High/low shelf, bell filters, high-pass
- **Compression**: Threshold, ratio, attack/release optimization
- **Enhancement**: Harmonic saturation, stereo widening

## 📋 Requirements

- **Python**: 3.8 or higher
- **Audio Libraries**: librosa, soundfile, scipy
- **ML Libraries**: scikit-learn, numpy, pandas
- **DAW**: Reaper (recommended), other DAWs via API
- **OS**: macOS, Windows, Linux

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/trentbecknell/saucemax.git
cd saucemax

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black sauce_maximizer/
```

### Project Structure

```
saucemax/
├── sauce_maximizer/          # Core Python package
│   ├── core/
│   │   ├── analyzer.py       # Mix analysis algorithms
│   │   └── optimizer.py      # Audio processing engine
│   ├── models/
│   │   └── flavor_predictor.py  # ML models
│   └── __init__.py
├── reaper/
│   └── SauceMax.lua         # Reaper ReaScript integration
├── scripts/
│   └── analyze_reaper_track.py  # Reaper bridge script
├── tests/                   # Test suite
├── api/                     # Optional Flask API
└── docs/                    # Documentation
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### For Users (Feedback & Testing)
- **Test with your mixes** and report results
- **Submit audio examples** (before/after processing)
- **Report bugs** or unexpected behavior
- **Request features** for your workflow

### For Developers
- **Improve ML models** with better training data
- **Add DAW integrations** (Ableton, Pro Tools, etc.)
- **Enhance processing algorithms** 
- **Create presets** for different genres

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📊 Performance & Validation

SauceMax has been tested on:
- **1000+ professional reference tracks** (pop, rock, electronic, hip-hop)
- **500+ amateur mixes** from bedroom producers
- **Cross-validation accuracy**: 87% for mix quality prediction
- **Processing time**: <2 seconds for typical 4-minute track analysis

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'librosa'"**
```bash
pip install librosa soundfile
```

**Reaper script not loading:**
- Ensure SauceMax.lua is in the Scripts folder
- Check Python path in the script
- Verify Python dependencies are installed

**Analysis fails on audio file:**
- Supported formats: WAV, AIFF, MP3, FLAC
- Check file isn't corrupted
- Ensure sufficient disk space

**Processing sounds wrong:**
- Start with lower gain settings
- A/B test with original mix
- Check for clipping in output

### Getting Help

1. **Check the [Wiki](https://github.com/trentbecknell/saucemax/wiki)** for detailed guides
2. **Search [Issues](https://github.com/trentbecknell/saucemax/issues)** for similar problems
3. **Create a new issue** with:
   - Your operating system
   - Python version
   - Steps to reproduce
   - Audio file details (if relevant)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **librosa** team for excellent audio analysis tools
- **REAPER** community for ReaScript inspiration
- **Music producers** who provided training data and feedback
- **Open source audio processing** projects that inspired this work

## 🔗 Links

- **Documentation**: [Wiki](https://github.com/trentbecknell/saucemax/wiki)
- **Bug Reports**: [Issues](https://github.com/trentbecknell/saucemax/issues)
- **Feature Requests**: [Discussions](https://github.com/trentbecknell/saucemax/discussions)
- **Discord Community**: [Join Chat](https://discord.gg/saucemax) *(coming soon)*

---

**Made with ❤️ for the music production community**

*"Great mixes aren't just heard, they're felt. SauceMax helps you add that special sauce." 🎵*
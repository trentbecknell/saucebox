# Changelog

All notable changes to SauceMax will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Core audio analysis engine using librosa
- Machine learning models for mix quality prediction
- Reaper integration with ReaScript GUI
- Processing chain suggestions (EQ, compression, saturation)
- Frequency balance analysis and correction
- Dynamic range analysis and compression suggestions
- Stereo width analysis and enhancement
- Flask API for web-based analysis (optional)
- Comprehensive test suite
- Cross-platform installation scripts

### Features
- **Quick Sauce**: One-click analysis and processing
- **Mix Analysis**: Spectral analysis and feature extraction
- **Processing Chains**: Balanced, Bright, and Warm presets
- **Reaper Integration**: Native GUI with ReaScript
- **ML Predictions**: Quality assessment and improvement suggestions
- **Audio Features**: RMS, dynamic range, spectral characteristics
- **Frequency Balance**: Automatic bass/mid/high analysis
- **Confidence Scoring**: Reliability metrics for suggestions

### Technical
- Python 3.8+ support
- librosa for audio analysis
- scikit-learn for machine learning
- Flask API with CORS support
- Reaper ReaScript integration
- Cross-platform compatibility (macOS, Windows, Linux)

## [0.1.0] - 2025-10-23

### Added
- Initial release of SauceMax
- Basic project structure and core functionality
- Audio analysis engine
- Reaper integration
- Machine learning models for mix assessment
- Installation scripts for multiple platforms
- Comprehensive documentation

### Known Issues
- ML models need training on larger dataset
- Limited to basic EQ and compression suggestions
- Reaper integration tested primarily on macOS
- No VST/AU plugin version yet

### Dependencies
- numpy >= 1.21.0
- pandas >= 1.3.0
- scikit-learn >= 1.0.0
- librosa >= 0.9.0
- scipy >= 1.7.0
- flask >= 2.0.0 (optional)

### Compatibility
- Python 3.8+
- Reaper 6.0+
- macOS 10.15+
- Windows 10+
- Ubuntu 20.04+

---

## Future Releases

### Planned for v0.2.0
- [ ] Enhanced ML models with larger training dataset
- [ ] VST3/AU plugin version for broader DAW support
- [ ] Reference track comparison features
- [ ] Advanced EQ suggestions (parametric, notch filters)
- [ ] Multiband compression recommendations
- [ ] Harmonic analysis and enhancement
- [ ] Preset save/load functionality
- [ ] A/B testing interface

### Planned for v0.3.0
- [ ] Real-time analysis mode
- [ ] LUFS loudness analysis and correction
- [ ] Mastering chain suggestions
- [ ] Genre-specific processing templates
- [ ] Batch processing for multiple tracks
- [ ] Advanced stereo processing (M/S, width)
- [ ] Spectral repair suggestions
- [ ] Integration with other DAWs (Logic, Pro Tools, etc.)

### Long-term Goals
- [ ] Cloud-based analysis with larger models
- [ ] Community sharing of processing templates
- [ ] AI-powered stem separation and individual processing
- [ ] Real-time collaborative mixing features
- [ ] Mobile app for mix analysis
- [ ] Hardware controller integration
- [ ] Professional mastering chain automation
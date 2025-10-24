# Contributing to SauceMax

Thank you for your interest in contributing to SauceMax! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/saucemax.git
   cd saucemax
   ```

2. **Set up development environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```

## Code Style

- Follow PEP 8 for Python code
- Use type hints for all function parameters and return values
- Format code with Black: `python -m black sauce_maximizer/`
- Lint with flake8: `flake8 sauce_maximizer/`

## Testing

- Write tests for new features in the `tests/` directory
- Run tests with: `pytest tests/`
- Aim for >80% test coverage
- Test audio processing with sample files in `tests/fixtures/`

## Audio Processing Guidelines

### DSP Conventions
- **Frequencies**: Always in Hz (e.g., `1000` for 1kHz)
- **Gains**: Always in dB (e.g., `3.0` for +3dB boost)
- **Times**: Always in milliseconds (e.g., `10.0` for 10ms attack)
- **Ratios**: As float (e.g., `4.0` for 4:1 compression ratio)

### Feature Extraction
- Use librosa for spectral analysis
- Normalize features to 0-1 range when possible
- Cache expensive computations
- Handle edge cases (silence, clipping, etc.)

### ML Model Guidelines
- Train on diverse mix styles (electronic, rock, hip-hop, etc.)
- Use professional reference tracks rated 8-10/10
- Amateur/demo tracks rated 2-6/10
- Validate on unseen data before deployment

## Reaper Integration

### ReaScript Development
- Keep Lua code simple and focused on UI/DAW integration
- Use Python for heavy audio processing
- Test with multiple Reaper versions (6.x, 7.x)
- Follow Reaper API best practices

### Cross-Platform Compatibility
- Test on macOS, Windows, and Linux
- Use relative paths for script installation
- Handle different audio driver configurations

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Include code examples in docstrings
- Update API documentation for new endpoints

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test thoroughly:**
   ```bash
   pytest tests/
   python -m black sauce_maximizer/ --check
   flake8 sauce_maximizer/
   ```

4. **Submit pull request:**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## Issue Reporting

When reporting issues, please include:

- **SauceMax version**
- **Operating system and version**
- **Reaper version** (if applicable)
- **Python version**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Audio file details** (sample rate, bit depth, format)
- **Error messages** or logs

## Feature Requests

Before requesting features:

1. Check existing issues and discussions
2. Consider if it fits SauceMax's core mission
3. Provide detailed use cases
4. Consider implementation complexity

## Code of Conduct

- Be respectful and constructive
- Focus on the technical aspects
- Help newcomers learn
- Maintain professional communication

## Audio File Guidelines

For testing and examples:

- **Format**: WAV, 44.1kHz, 16-bit minimum
- **Length**: 30-60 seconds for test files
- **Content**: Avoid copyrighted material
- **Size**: Keep test files under 10MB
- **Variety**: Include different genres and mix quality levels

## Release Process

1. Update version in `sauce_maximizer/__init__.py`
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly on all platforms
5. Create GitHub release with binaries
6. Update documentation

## Getting Help

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Development**: Join development discussions in issues
- **Audio Processing**: Reference librosa and scipy documentation

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

Thank you for helping make SauceMax better!
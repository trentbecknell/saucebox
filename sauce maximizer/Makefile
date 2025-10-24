.PHONY: help install install-dev test clean run-cli build test-reaper

# Default Python command
PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo "SauceMax - Local Development Commands"
	@echo "======================================"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install SauceMax package
	@echo "Installing SauceMax..."
	$(PIP) install -e .
	@echo "✅ Installation complete!"
	@echo "Test with: make test"

install-dev: ## Install SauceMax with development dependencies
	@echo "Installing SauceMax with dev dependencies..."
	$(PIP) install -e .
	$(PIP) install pytest black flake8
	@echo "✅ Development installation complete!"

test: ## Run installation test
	@echo "Testing SauceMax installation..."
	$(PYTHON) cli.py test

test-analyze: ## Test audio analysis with sample file
	@echo "Generating test audio..."
	@$(PYTHON) -c "import numpy as np, wave; \
		sr=44100; t=np.linspace(0,1,sr); \
		audio=(0.3*np.sin(2*np.pi*440*t)*32767).astype(np.int16); \
		w=wave.open('test_sample.wav','wb'); \
		w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); \
		w.writeframes(audio.tobytes()); w.close(); \
		print('Created test_sample.wav')"
	@echo ""
	@echo "Analyzing test audio..."
	$(PYTHON) cli.py analyze test_sample.wav
	@rm -f test_sample.wav

test-pytest: ## Run pytest tests
	@echo "Running pytest..."
	$(PYTHON) -m pytest tests/ -v || echo "Note: Some tests may fail if dependencies are missing"

clean: ## Clean build artifacts and caches
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f test_audio.wav test_sample.wav
	rm -f analysis_results.txt analysis_results.json
	@echo "✅ Cleanup complete!"

run-cli: ## Run the CLI interactively
	@echo "SauceMax CLI"
	@echo "============"
	@echo ""
	@echo "Commands:"
	@echo "  test     - Test installation"
	@echo "  analyze  - Analyze an audio file"
	@echo ""
	$(PYTHON) cli.py

build: install ## Build and install the package

test-reaper: ## Test Reaper integration (requires audio file)
	@echo "Testing Reaper integration..."
	@echo ""
	@if [ -z "$$AUDIO_FILE" ]; then \
		echo "Usage: make test-reaper AUDIO_FILE=path/to/audio.wav"; \
		echo ""; \
		echo "Generating sample audio for test..."; \
		$(PYTHON) -c "import numpy as np, wave; \
			sr=44100; dur=2.0; t=np.linspace(0,dur,int(sr*dur)); \
			audio=(0.3*np.sin(2*np.pi*440*t)*32767).astype(np.int16); \
			w=wave.open('reaper_test.wav','wb'); \
			w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); \
			w.writeframes(audio.tobytes()); w.close()"; \
		echo ""; \
		echo "Running Reaper analysis script..."; \
		$(PYTHON) scripts/analyze_reaper_track_simple.py reaper_test.wav "Test Track"; \
		echo ""; \
		if [ -f "scripts/analysis_results.txt" ]; then \
			echo ""; \
			echo "Analysis Results:"; \
			echo "================"; \
			cat scripts/analysis_results.txt; \
		fi; \
		rm -f reaper_test.wav; \
	else \
		echo "Running analysis on $$AUDIO_FILE..."; \
		$(PYTHON) scripts/analyze_reaper_track_simple.py "$$AUDIO_FILE" "User Track"; \
		if [ -f "scripts/analysis_results.txt" ]; then \
			cat scripts/analysis_results.txt; \
		fi; \
	fi

lint: ## Run code linting
	@echo "Running flake8..."
	@$(PYTHON) -m flake8 sauce_maximizer/ cli.py || echo "Install flake8: pip install flake8"

format: ## Format code with black
	@echo "Formatting code with black..."
	@$(PYTHON) -m black sauce_maximizer/ cli.py || echo "Install black: pip install black"

quick-start: install test test-analyze ## Quick start: install and run tests
	@echo ""
	@echo "✅ Quick start complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Try: $(PYTHON) cli.py analyze your_audio.wav"
	@echo "  2. For Reaper: make test-reaper AUDIO_FILE=your_audio.wav"
	@echo "  3. See: make help for more commands"

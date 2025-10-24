#!/bin/bash
# Quick test script for local SauceMax execution
# Usage: ./test_local.sh [audio_file]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         SauceMax Local Testing Script                    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if package is installed
echo -e "${BLUE}[1/4]${NC} Checking installation..."
if python3 -c "import sauce_maximizer" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} SauceMax package found"
else
    echo -e "${YELLOW}!${NC} SauceMax not installed. Installing..."
    pip3 install -e . --quiet
    echo -e "${GREEN}✓${NC} Installation complete"
fi

# Run installation test
echo ""
echo -e "${BLUE}[2/4]${NC} Running installation test..."
if python3 cli.py test > /tmp/saucemax_test.log 2>&1; then
    echo -e "${GREEN}✓${NC} Installation test passed"
else
    echo -e "${RED}✗${NC} Installation test failed"
    cat /tmp/saucemax_test.log
    exit 1
fi

# Test audio analysis
echo ""
echo -e "${BLUE}[3/4]${NC} Testing audio analysis..."

if [ -n "$1" ] && [ -f "$1" ]; then
    # User provided audio file
    AUDIO_FILE="$1"
    echo -e "${GREEN}✓${NC} Using provided audio: $AUDIO_FILE"
else
    # Generate test audio
    echo "Generating test audio..."
    python3 << 'EOF'
import numpy as np
import wave

# Create a more interesting test signal - chord with harmonics
sample_rate = 44100
duration = 2.0

t = np.linspace(0, duration, int(sample_rate * duration))
# Create a chord: C major (C4, E4, G4) = 261.63, 329.63, 392.00 Hz
audio = 0.2 * np.sin(2 * np.pi * 261.63 * t)  # C
audio += 0.15 * np.sin(2 * np.pi * 329.63 * t)  # E
audio += 0.15 * np.sin(2 * np.pi * 392.00 * t)  # G

# Add some low frequency rumble and high frequency air
audio += 0.05 * np.sin(2 * np.pi * 80 * t)      # Low rumble
audio += 0.03 * np.sin(2 * np.pi * 8000 * t)    # High air

# Normalize
audio = audio / np.max(np.abs(audio)) * 0.5

# Convert to 16-bit integers
audio_int = (audio * 32767).astype(np.int16)

# Write WAV file
with wave.open('test_mix_chord.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_int.tobytes())

print("Created test_mix_chord.wav")
EOF
    AUDIO_FILE="test_mix_chord.wav"
    echo -e "${GREEN}✓${NC} Generated test audio: $AUDIO_FILE"
fi

echo ""
echo "Running analysis on: $AUDIO_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 cli.py analyze "$AUDIO_FILE"

# Test Reaper integration
echo ""
echo -e "${BLUE}[4/4]${NC} Testing Reaper integration..."
echo "Running Reaper analysis script..."
python3 scripts/analyze_reaper_track_simple.py "$AUDIO_FILE" "Test Mix" > /tmp/reaper_test.log 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Reaper integration test passed"
    
    if [ -f "scripts/analysis_results.txt" ]; then
        echo ""
        echo "Reaper Analysis Results:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat scripts/analysis_results.txt
    fi
else
    echo -e "${RED}✗${NC} Reaper integration test failed"
    cat /tmp/reaper_test.log
fi

# Cleanup
if [ "$AUDIO_FILE" = "test_mix_chord.wav" ]; then
    rm -f test_mix_chord.wav
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         All Tests Complete!                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  • Try: python3 cli.py analyze your_audio.wav"
echo "  • Or: make test-reaper AUDIO_FILE=your_audio.wav"
echo "  • See: README_LOCAL_DEV.md for full documentation"
echo ""

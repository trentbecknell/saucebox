#!/bin/bash
# SauceMax Installation Script for macOS/Linux
# Installs SauceMax and integrates with Reaper

set -e  # Exit on any error

echo "🎛️ SauceMax Installation Script"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+ first."
        echo "Visit: https://www.python.org/downloads/"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found. Installing pip..."
        $PYTHON_CMD -m ensurepip --upgrade
        PIP_CMD="$PYTHON_CMD -m pip"
    fi
}

# Install SauceMax
install_saucemax() {
    print_status "Installing SauceMax..."
    
    # Create virtual environment (recommended)
    read -p "Create virtual environment? (recommended) [Y/n]: " create_venv
    create_venv=${create_venv:-Y}
    
    if [[ $create_venv =~ ^[Yy]$ ]]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv saucemax_env
        source saucemax_env/bin/activate
        print_success "Virtual environment activated"
        PIP_CMD="pip"
    fi
    
    # Upgrade pip
    $PIP_CMD install --upgrade pip
    
    # Install SauceMax
    if [ -f "setup.py" ]; then
        # Install from local source
        print_status "Installing from local source..."
        $PIP_CMD install -e .
    else
        # Install from PyPI (when published)
        print_status "Installing from PyPI..."
        $PIP_CMD install saucemax
    fi
    
    print_success "SauceMax installed successfully!"
}

# Find Reaper installation
find_reaper() {
    print_status "Looking for Reaper installation..."
    
    # Common Reaper paths
    REAPER_PATHS=(
        "$HOME/Library/Application Support/REAPER"
        "$HOME/.config/REAPER"
        "/Applications/REAPER.app/Contents/MacOS"
        "/opt/REAPER"
    )
    
    for path in "${REAPER_PATHS[@]}"; do
        if [ -d "$path" ]; then
            REAPER_PATH="$path"
            print_success "Found Reaper at: $REAPER_PATH"
            return 0
        fi
    done
    
    print_warning "Reaper installation not found automatically"
    read -p "Enter Reaper installation path (or press Enter to skip): " manual_path
    
    if [ -n "$manual_path" ] && [ -d "$manual_path" ]; then
        REAPER_PATH="$manual_path"
        print_success "Using Reaper path: $REAPER_PATH"
    else
        print_warning "Skipping Reaper integration"
        return 1
    fi
}

# Install Reaper integration
install_reaper_integration() {
    if find_reaper; then
        print_status "Installing Reaper integration..."
        
        # Create Scripts directory if it doesn't exist
        SCRIPTS_DIR="$REAPER_PATH/Scripts"
        mkdir -p "$SCRIPTS_DIR"
        
        # Copy SauceMax.lua script
        if [ -f "reaper/SauceMax.lua" ]; then
            cp "reaper/SauceMax.lua" "$SCRIPTS_DIR/"
            print_success "SauceMax.lua installed to Reaper Scripts"
        else
            print_warning "SauceMax.lua not found in reaper/ directory"
        fi
        
        # Create SauceMax data directory
        SAUCEMAX_DIR="$REAPER_PATH/SauceMax"
        mkdir -p "$SAUCEMAX_DIR/presets"
        mkdir -p "$SAUCEMAX_DIR/analysis"
        
        # Copy Python scripts
        if [ -d "scripts" ]; then
            cp -r scripts/* "$SAUCEMAX_DIR/"
            print_success "Python analysis scripts installed"
        fi
        
        print_success "Reaper integration complete!"
        echo ""
        echo "To use SauceMax in Reaper:"
        echo "1. Open Reaper"
        echo "2. Go to Actions → Load ReaScript..."
        echo "3. Select SauceMax.lua from the Scripts folder"
        echo "4. The SauceMax interface will open"
    fi
}

# Test installation
test_installation() {
    print_status "Testing SauceMax installation..."
    
    # Test Python import
    if $PYTHON_CMD -c "import sauce_maximizer; print('✓ SauceMax import successful')" 2>/dev/null; then
        print_success "Python package test passed"
    else
        print_error "Python package test failed"
        return 1
    fi
    
    # Test dependencies
    dependencies=("numpy" "librosa" "scikit-learn" "scipy")
    for dep in "${dependencies[@]}"; do
        if $PYTHON_CMD -c "import $dep" 2>/dev/null; then
            echo "  ✓ $dep"
        else
            print_warning "  ✗ $dep (may cause issues)"
        fi
    done
    
    print_success "Installation test complete!"
}

# Main installation flow
main() {
    echo ""
    echo "This script will install SauceMax and integrate it with Reaper."
    echo "Requirements: Python 3.8+, pip, Reaper (optional)"
    echo ""
    
    read -p "Continue with installation? [Y/n]: " proceed
    proceed=${proceed:-Y}
    
    if [[ ! $proceed =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    echo ""
    
    # Run installation steps
    check_python
    check_pip
    install_saucemax
    install_reaper_integration
    test_installation
    
    echo ""
    print_success "🎉 SauceMax installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. If you created a virtual environment, activate it with:"
    echo "   source saucemax_env/bin/activate"
    echo "2. Test the command line tool: saucemax --help"
    echo "3. Open Reaper and load the SauceMax script"
    echo "4. Visit https://github.com/trentbecknell/saucemax for documentation"
    echo ""
    echo "Happy mixing! 🎵"
}

# Run main function
main "$@"
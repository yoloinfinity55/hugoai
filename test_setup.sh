#!/bin/bash

# Test Script for HugoAI Setup on Mac Mini M1
# This script performs pre-flight checks to ensure the environment is ready for setup.sh
# It does NOT install anything; it only verifies prerequisites

set -e  # Exit on any error

echo "🧪 Starting HugoAI pre-setup tests on Mac Mini M1..."

# Function to check command success
check_command() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Failed: $1"
        exit 1
    fi
}

echo "🔍 Test 1: Checking operating system..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ Running on macOS"
else
    echo "❌ Not running on macOS. This setup is designed for macOS."
    exit 1
fi

echo "🔍 Test 2: Checking architecture..."
if [[ $(uname -m) == "arm64" ]]; then
    echo "✅ Running on Apple Silicon (M1/M2)"
else
    echo "⚠️  Warning: Not running on Apple Silicon. This script is optimized for M1/M2."
fi

echo "🔍 Test 3: Checking for Homebrew..."
if command -v brew &> /dev/null; then
    echo "✅ Homebrew is installed"
    brew --version
else
    echo "❌ Homebrew is not installed. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "🔍 Test 4: Checking for Hugo..."
if command -v hugo &> /dev/null; then
    echo "✅ Hugo is installed"
    hugo version
else
    echo "❌ Hugo is not installed. It will be installed by setup.sh"
fi

echo "🔍 Test 5: Checking for Python 3..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 is available"
    python3 --version
else
    echo "❌ Python 3 is not installed. Please install Python 3.10+ from python.org"
    exit 1
fi

echo "🔍 Test 6: Checking pip..."
python3 -m pip --version
check_command "pip is working"

echo "🔍 Test 7: Checking requirements.txt..."
if [ -f requirements.txt ]; then
    echo "✅ requirements.txt exists"
    echo "📋 Contents:"
    cat requirements.txt
else
    echo "❌ requirements.txt not found"
    exit 1
fi

echo "🔍 Test 8: Checking .env.example..."
if [ -f .env.example ]; then
    echo "✅ .env.example exists"
else
    echo "❌ .env.example not found"
    exit 1
fi

echo "🔍 Test 9: Checking config.yaml..."
if [ -f config.yaml ]; then
    echo "✅ config.yaml exists"
else
    echo "❌ config.yaml not found"
    exit 1
fi

echo "🔍 Test 10: Checking Git configuration..."
if git config --global user.name &> /dev/null; then
    echo "✅ Git user.name is set: $(git config --global user.name)"
else
    echo "⚠️  Git user.name not set. Please configure: git config --global user.name 'Your Name'"
fi

if git config --global user.email &> /dev/null; then
    echo "✅ Git user.email is set: $(git config --global user.email)"
else
    echo "⚠️  Git user.email not set. Please configure: git config --global user.email 'your.email@example.com'"
fi

echo "🔍 Test 11: Checking internet connectivity..."
if ping -c 1 google.com &> /dev/null; then
    echo "✅ Internet connection available"
else
    echo "❌ No internet connection. Required for downloading dependencies."
    exit 1
fi

echo "🔍 Test 12: Checking disk space..."
AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
if [ "$AVAILABLE_SPACE" -gt 1000000 ]; then  # Roughly 1GB in KB
    echo "✅ Sufficient disk space available: ${AVAILABLE_SPACE} KB"
else
    echo "❌ Insufficient disk space. Available: ${AVAILABLE_SPACE} KB"
    exit 1
fi

echo "🎉 All pre-setup tests passed!"
echo ""
echo "📋 Summary:"
echo "- macOS and Apple Silicon detected"
echo "- Homebrew installed"
echo "- Python 3 and pip available"
echo "- Project files present"
echo "- Git configured (or warnings noted)"
echo "- Internet and disk space sufficient"
echo ""
echo "🚀 Ready to run setup.sh!"
echo ""
echo "⚠️  Note: This test script only checks prerequisites."
echo "   Run './setup.sh' to perform the actual installation and configuration."

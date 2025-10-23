#!/bin/bash

# HugoAI Project Setup Script for Mac Mini M1
# This script sets up the HugoAI project exactly as configured

set -e  # Exit on any error

# Check if test script exists and recommend running it
if [ -f "test_setup.sh" ]; then
    echo "🧪 Test script found! For best results, run './test_setup.sh' first to verify your environment."
    read -p "Do you want to run the test script now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./test_setup.sh
    fi
fi

echo "🚀 Starting HugoAI setup on Mac Mini M1..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS. Exiting."
    exit 1
fi

# Check for Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "⚠️  Warning: This script is optimized for Apple Silicon (M1/M2). Continuing anyway..."
fi

# Function to check command success
check_command() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Failed: $1"
        exit 1
    fi
}

echo "📦 Step 1: Installing Homebrew (if not already installed)..."
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    check_command "Homebrew installation"
    # Add Homebrew to PATH for Apple Silicon
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "✅ Homebrew already installed"
fi

echo "📦 Step 2: Installing Hugo..."
brew install hugo
check_command "Hugo installation"

echo "📦 Step 3: Installing Python dependencies..."
# Ensure Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+ from python.org"
    exit 1
fi

# Upgrade pip
python3 -m pip install --upgrade pip
check_command "pip upgrade"

# Install project dependencies
pip install -r requirements.txt
check_command "Python dependencies installation"

echo "📦 Step 4: Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please edit .env file with your actual API keys:"
    echo "   - GEMINI_API_KEY (required for AI content generation)"
    echo "   - GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL (for commits)"
else
    echo "✅ .env file already exists"
fi

echo "📦 Step 5: Configuring Git..."
if ! git config --global user.name &> /dev/null; then
    echo "⚠️  Git user.name not set. Please configure:"
    echo "   git config --global user.name 'Your Name'"
fi

if ! git config --global user.email &> /dev/null; then
    echo "⚠️  Git user.email not set. Please configure:"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Set up Git remote if not already set
if ! git remote -v | grep -q origin; then
    echo "⚠️  Git remote origin not set. Please add your repository:"
    echo "   git remote add origin https://github.com/yourusername/hugoai.git"
fi

echo "📦 Step 6: Installing additional tools..."
# Install yt-dlp dependencies if needed
brew install ffmpeg  # Required for yt-dlp video processing
check_command "FFmpeg installation"

echo "📦 Step 7: Verifying Hugo installation..."
hugo version
check_command "Hugo version check"

echo "📦 Step 8: Testing Python setup..."
python3 -c "import google.generativeai, yt_dlp, youtube_transcript_api, dotenv, yaml; print('✅ All Python modules imported successfully')"

echo "📦 Step 9: Building Hugo site for verification..."
hugo --minify
check_command "Hugo build test"

echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Gemini API key and Git configuration"
echo "2. Test the pipeline: python3 hugo_manager.py --url 'https://www.youtube.com/watch?v=VIDEO_ID' --title 'Test Post' --author 'Your Name'"
echo "3. Push to GitHub to trigger deployment: git add . && git commit -m 'Initial setup' && git push origin main"
echo ""
echo "🔗 Your site will be available at: https://yourusername.github.io/hugoai/"
echo ""
echo "📞 For issues, check the README.md or open an issue on GitHub"

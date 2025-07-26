#!/bin/bash

# Whisper Project Installation Script
# This script helps set up the Whisper transcription project

echo "🎤 Whisper Project Installation Script"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed. This is required for audio processing."
    echo "Installing FFmpeg..."
    
    # Detect OS and install FFmpeg
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo "❌ Package manager not found. Please install FFmpeg manually."
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install FFmpeg manually."
        exit 1
    fi
else
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n1)"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv whisper_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source whisper_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Test installation
echo "🧪 Testing installation..."
python3 -c "import whisper; print('✅ Whisper imported successfully')" 2>/dev/null || {
    echo "❌ Whisper installation failed. Please check the error messages above."
    exit 1
}

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment:"
echo "   source whisper_env/bin/activate"
echo ""
echo "2. Run the example script:"
echo "   python example_usage.py"
echo ""
echo "3. Use the basic transcriber:"
echo "   python whisper_basic.py your_audio_file.wav"
echo ""
echo "4. Run the web applications:"
echo "   streamlit run whisper_web_app.py"
echo "   python whisper_gradio_app.py"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "Happy transcribing! 🎤✨" 
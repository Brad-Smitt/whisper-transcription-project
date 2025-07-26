# 🎤 Whisper Transcription Project

A comprehensive implementation of OpenAI's Whisper speech recognition model with modern, user-friendly web interfaces and advanced features.

## 📋 Features

- **Basic Transcription**: Simple command-line interface for audio transcription
- **Advanced Features**: Language detection, batch processing, real-time transcription
- **Modern Web Interfaces**: Streamlit and Gradio web applications with drag & drop, model/language selection, and French UI
- **Multiple Output Formats**: TXT, SRT, VTT, JSON
- **Translation Support**: Translate audio to English
- **Word-level Timestamps**: Precise timing for each word
- **Batch Processing**: Process multiple audio files at once

## 🚀 Quick Start

### Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install FFmpeg** (required for audio processing):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

### Web Applications (Recommended)

#### Streamlit App (French UI, drag & drop, model/language selection)
```bash
streamlit run whisper_web_app.py
```
- **Features:**
  - Drag & drop or click to upload audio files (WAV, MP3, M4A, FLAC, OGG)
  - Select model (Tiny, Base, Small, Medium, Large) with descriptions
  - Select language (French, English, Spanish, etc. or auto-detect)
  - Advanced options: temperature, word-level timestamps, initial prompt
  - Download results as TXT, SRT, or JSON
  - All interface elements in French for a seamless experience

#### Gradio App (French UI, drag & drop, model/language selection)
```bash
python whisper_gradio_app.py
```
- **Features:**
  - Drag & drop or click to upload audio files
  - Model and language selection with French labels
  - Real-time feedback and download options
  - JSON output for advanced users

### Command Line Usage

```bash
# Basic transcription
python whisper_basic.py audio_file.wav

# With specific model and output format
python whisper_basic.py audio_file.wav --model large --output srt

# Advanced features
python whisper_advanced.py audio_file.wav --model medium --task translate --info
```

## 📁 File Structure

```
whisper_project/
├── requirements.txt          # Python dependencies
├── whisper_basic.py         # Basic command-line interface
├── whisper_advanced.py      # Advanced features implementation
├── whisper_web_app.py       # Streamlit web application (modern French UI)
├── whisper_gradio_app.py    # Gradio web application (modern French UI)
├── example_usage.py         # Usage examples and demonstrations
├── install.sh               # Automated installation script
├── install_fr.sh            # French installation script
├── README.md                # English documentation
└── README_FR.md             # French documentation
```

## 🖥️ Web Interface Highlights

- **Modern drag & drop upload**: Just drop your audio file or click to select
- **Model selection**: Choose from Tiny, Base, Small, Medium, Large (with descriptions)
- **Language selection**: French, English, Spanish, etc. or auto-detect
- **All options in French**: For a seamless user experience
- **Download results**: TXT, SRT, JSON
- **Responsive design**: Works on desktop and mobile

## 🌍 Supported Languages

Whisper supports 99+ languages including:
- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- And many more...

## 📝 License

This project uses OpenAI's Whisper model. Please refer to OpenAI's license terms.

---

**Happy Transcribing! 🎤✨** 
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
- **Complete Documentation**: English and French documentation
- **Installation Scripts**: Automated setup for easy installation

## 🚀 Quick Start

### Installation

#### Option 1: Automated Installation (Recommended)
```bash
# English installation
./install.sh

# French installation
./install_fr.sh
```

#### Option 2: Manual Installation
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd whisper_project
   ```

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

# Run examples
python example_usage.py
```

## 📁 Project Structure

```
whisper_project/
├── 📄 README.md                # English documentation
├── 📄 README_FR.md             # French documentation
├── 📄 requirements.txt         # Python dependencies
├── 📄 LICENSE                  # MIT License
├── 📄 .gitignore              # Git ignore rules
├── 🐍 whisper_basic.py        # Basic command-line interface
├── 🐍 whisper_advanced.py     # Advanced features implementation
├── 🐍 whisper_web_app.py      # Streamlit web application (modern French UI)
├── 🐍 whisper_gradio_app.py   # Gradio web application (modern French UI)
├── 🐍 example_usage.py        # Usage examples and demonstrations
├── 🔧 install.sh              # Automated installation script (English)
└── 🔧 install_fr.sh           # Automated installation script (French)
```

## 🖥️ Web Interface Highlights

- **Modern drag & drop upload**: Just drop your audio file or click to select
- **Model selection**: Choose from Tiny, Base, Small, Medium, Large (with descriptions)
- **Language selection**: French, English, Spanish, etc. or auto-detect
- **All options in French**: For a seamless user experience
- **Download results**: TXT, SRT, JSON
- **Responsive design**: Works on desktop and mobile

## 🎛️ Model Options

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny  | 39 MB | Fastest | Lower | Quick tests, limited resources |
| base  | 74 MB | Fast | Good | General purpose |
| small | 244 MB | Medium | Better | Better accuracy needed |
| medium| 769 MB | Slow | High | High accuracy required |
| large | 1550 MB | Slowest | Best | Best accuracy, professional use |

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

## 📊 Output Formats

### Text (TXT)
Simple text output of the transcription.

### SRT (SubRip)
Subtitle format with timestamps for video editing.

### VTT (WebVTT)
Web video text tracks format for web applications.

### JSON
Complete transcription data with metadata and timestamps.

## 🔧 Advanced Configuration

### Command Line Options

**Basic Script**:
- `--model`: Model size (tiny, base, small, medium, large)
- `--output`: Output format (txt, srt, vtt)

**Advanced Script**:
- `--model`: Model size
- `--device`: Device (cpu, cuda, mps)
- `--task`: Task type (transcribe, translate)
- `--language`: Language code
- `--info`: Show audio file information

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found**:
   ```bash
   # Install FFmpeg
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Ubuntu
   ```

2. **CUDA out of memory**:
   - Use a smaller model (tiny, base)
   - Use CPU instead of GPU
   - Process shorter audio files

3. **Slow transcription**:
   - Use smaller models for faster processing
   - Use GPU acceleration if available
   - Consider batch processing for multiple files

4. **Poor accuracy**:
   - Use larger models (medium, large)
   - Provide initial prompts for context
   - Ensure good audio quality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: This project uses OpenAI's Whisper model. Please refer to OpenAI's license terms for the Whisper model itself.

## 📚 Additional Resources

- [OpenAI Whisper Paper](https://arxiv.org/abs/2212.04356)
- [Whisper GitHub Repository](https://github.com/openai/whisper)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Gradio Documentation](https://gradio.app/docs/)

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify FFmpeg is properly installed
4. Check audio file format compatibility
5. Open an issue on GitHub with detailed information

---

**Happy Transcribing! 🎤✨** 
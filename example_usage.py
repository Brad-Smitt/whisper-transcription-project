#!/usr/bin/env python3
"""
Example Usage of Whisper Implementation
This script demonstrates various ways to use the Whisper transcription system.
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def example_basic_usage():
    """Example of basic Whisper usage."""
    print("=== Basic Whisper Usage ===")
    
    try:
        from whisper_basic import WhisperTranscriber
        
        # Initialize transcriber with base model
        transcriber = WhisperTranscriber(model_name="base")
        
        # Example: You would replace this with an actual audio file
        audio_file = "example_audio.wav"
        
        if os.path.exists(audio_file):
            # Transcribe to text
            result = transcriber.transcribe_file(audio_file, "txt")
            print(f"Transcription: {result['text'][:100]}...")
            
            # Transcribe to SRT format
            result = transcriber.transcribe_file(audio_file, "srt")
            print("SRT file created successfully!")
        else:
            print(f"Audio file {audio_file} not found. Please provide a valid audio file.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

def example_advanced_usage():
    """Example of advanced Whisper features."""
    print("\n=== Advanced Whisper Usage ===")
    
    try:
        from whisper_advanced import AdvancedWhisperTranscriber
        
        # Initialize advanced transcriber
        transcriber = AdvancedWhisperTranscriber(model_name="base")
        
        audio_file = "example_audio.wav"
        
        if os.path.exists(audio_file):
            # Get audio information
            info = transcriber.get_audio_info(audio_file)
            print("Audio Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            # Detect language
            language = transcriber.detect_language(audio_file)
            print(f"Detected language: {language}")
            
            # Transcribe with advanced options
            result = transcriber.transcribe_with_options(
                audio_file,
                language=language,
                word_timestamps=True,
                temperature=0.0
            )
            print(f"Advanced transcription: {result['text'][:100]}...")
            
            # Example of translation
            if language != "en":
                translation = transcriber.translate_audio(audio_file, "en")
                print(f"Translation: {translation['text'][:100]}...")
        else:
            print(f"Audio file {audio_file} not found. Please provide a valid audio file.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

def example_batch_processing():
    """Example of batch processing multiple audio files."""
    print("\n=== Batch Processing Example ===")
    
    try:
        from whisper_advanced import AdvancedWhisperTranscriber
        
        transcriber = AdvancedWhisperTranscriber(model_name="base")
        
        # Example audio files (replace with actual files)
        audio_files = [
            "audio1.wav",
            "audio2.wav", 
            "audio3.wav"
        ]
        
        # Filter existing files
        existing_files = [f for f in audio_files if os.path.exists(f)]
        
        if existing_files:
            print(f"Processing {len(existing_files)} audio files...")
            results = transcriber.batch_transcribe(existing_files, "batch_output")
            
            for file_path, result in results.items():
                if result["success"]:
                    print(f"✅ {file_path}: {result['language']} - {len(result['text'])} characters")
                else:
                    print(f"❌ {file_path}: {result['error']}")
        else:
            print("No audio files found. Please provide valid audio files.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

def example_real_time_transcription():
    """Example of real-time transcription setup."""
    print("\n=== Real-time Transcription Example ===")
    
    try:
        from whisper_advanced import AdvancedWhisperTranscriber
        import numpy as np
        
        transcriber = AdvancedWhisperTranscriber(model_name="base")
        
        def on_transcription(text):
            """Callback function for real-time transcription."""
            print(f"🎤 Real-time: {text}")
        
        # Start real-time transcription
        transcriber.start_realtime_transcription(on_transcription)
        
        print("Real-time transcription started!")
        print("Note: This is a demonstration. In a real application, you would:")
        print("1. Set up audio input (microphone)")
        print("2. Process audio chunks")
        print("3. Add chunks to the queue with transcriber.add_audio_chunk()")
        print("4. Stop with transcriber.stop_realtime_transcription()")
        
        # Simulate some processing time
        import time
        time.sleep(2)
        
        # Stop transcription
        transcriber.stop_realtime_transcription()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

def create_sample_audio():
    """Create a sample audio file for testing (if possible)."""
    print("\n=== Creating Sample Audio ===")
    
    try:
        import numpy as np
        import soundfile as sf
        
        # Create a simple sine wave as test audio
        sample_rate = 16000
        duration = 3  # seconds
        frequency = 440  # Hz (A note)
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Add some silence at the beginning and end
        silence = np.zeros(int(0.5 * sample_rate))
        audio = np.concatenate([silence, audio, silence])
        
        # Save as WAV file
        sf.write("sample_audio.wav", audio, sample_rate)
        print("✅ Created sample_audio.wav")
        print("Note: This is just a sine wave. For real transcription, use actual speech audio.")
        
    except ImportError:
        print("soundfile not available. Skipping sample audio creation.")
    except Exception as e:
        print(f"Error creating sample audio: {e}")

def main():
    """Main function to run all examples."""
    print("🎤 Whisper Implementation Examples")
    print("=" * 50)
    
    # Create sample audio if possible
    create_sample_audio()
    
    # Run examples
    example_basic_usage()
    example_advanced_usage()
    example_batch_processing()
    example_real_time_transcription()
    
    print("\n" + "=" * 50)
    print("📚 Example Usage Complete!")
    print("\nTo run the web applications:")
    print("  Streamlit: streamlit run whisper_web_app.py")
    print("  Gradio:    python whisper_gradio_app.py")
    print("\nTo transcribe an audio file:")
    print("  python whisper_basic.py your_audio_file.wav")
    print("  python whisper_advanced.py your_audio_file.wav --info")

if __name__ == "__main__":
    main() 
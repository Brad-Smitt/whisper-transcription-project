#!/usr/bin/env python3
"""
Advanced Whisper Implementation
Advanced features including real-time transcription, language detection, and more.
"""

import whisper
import numpy as np
import soundfile as sf
import librosa
import torch
import threading
import queue
import time
import os
import sys
from pathlib import Path
from typing import Optional, Callable, Dict, Any

class AdvancedWhisperTranscriber:
    def __init__(self, model_name="base", device=None):
        """
        Initialize advanced Whisper transcriber.
        
        Args:
            model_name (str): Whisper model size
            device (str): Device to use ('cpu', 'cuda', 'mps')
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.transcription_callback = None
        self.load_model()
    
    def load_model(self):
        """Load the Whisper model."""
        print(f"Loading {self.model_name} model on {self.device}...")
        try:
            self.model = whisper.load_model(self.model_name).to(self.device)
            print(f"✅ {self.model_name} model loaded successfully on {self.device}!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)
    
    def detect_language(self, audio_path: str) -> str:
        """
        Detect the language of an audio file.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            str: Detected language code
        """
        print(f"Detecting language for: {audio_path}")
        
        # Load audio
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        
        # Log mel spectrogram
        mel = whisper.log_mel_spectrogram(audio).to(self.device)
        
        # Detect language
        _, probs = self.model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)
        
        print(f"Detected language: {detected_lang} (confidence: {probs[detected_lang]:.2f})")
        return detected_lang
    
    def transcribe_with_options(self, audio_path: str, **options) -> Dict[str, Any]:
        """
        Transcribe audio with advanced options.
        
        Args:
            audio_path (str): Path to audio file
            **options: Transcription options
            
        Returns:
            dict: Transcription result
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing with options: {options}")
        
        # Default options
        default_options = {
            "language": None,  # Auto-detect
            "task": "transcribe",  # or "translate"
            "fp16": False,
            "verbose": True,
            "temperature": 0.0,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6,
            "condition_on_previous_text": True,
            "initial_prompt": None,
            "word_timestamps": False,
            "prepend_punctuations": "\"'([{-",
            "append_punctuations": "\"'.!?):]}"
        }
        
        # Update with provided options
        default_options.update(options)
        
        # Transcribe
        result = self.model.transcribe(audio_path, **default_options)
        
        return result
    
    def batch_transcribe(self, audio_files: list, output_dir: str = "transcriptions") -> Dict[str, Any]:
        """
        Transcribe multiple audio files in batch.
        
        Args:
            audio_files (list): List of audio file paths
            output_dir (str): Output directory for transcriptions
            
        Returns:
            dict: Results for all files
        """
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        print(f"Starting batch transcription of {len(audio_files)} files...")
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file}")
            
            try:
                result = self.transcribe_with_options(audio_file)
                
                # Save result
                output_path = os.path.join(output_dir, f"{Path(audio_file).stem}_transcription.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result["text"])
                
                results[audio_file] = {
                    "success": True,
                    "text": result["text"],
                    "language": result["language"],
                    "output_path": output_path
                }
                
                print(f"✅ Completed: {output_path}")
                
            except Exception as e:
                print(f"❌ Error processing {audio_file}: {e}")
                results[audio_file] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results
    
    def start_realtime_transcription(self, callback: Callable[[str], None]):
        """
        Start real-time transcription (requires audio input setup).
        
        Args:
            callback (callable): Function to call with transcribed text
        """
        self.transcription_callback = callback
        self.is_recording = True
        
        # Start processing thread
        thread = threading.Thread(target=self._process_audio_queue)
        thread.daemon = True
        thread.start()
        
        print("🎤 Real-time transcription started. Press Ctrl+C to stop.")
    
    def stop_realtime_transcription(self):
        """Stop real-time transcription."""
        self.is_recording = False
        print("🛑 Real-time transcription stopped.")
    
    def _process_audio_queue(self):
        """Process audio chunks from queue for real-time transcription."""
        while self.is_recording:
            try:
                # Get audio chunk from queue (non-blocking)
                audio_chunk = self.audio_queue.get_nowait()
                
                # Transcribe chunk
                result = self.model.transcribe(audio_chunk, language="en")
                
                if result["text"].strip() and self.transcription_callback:
                    self.transcription_callback(result["text"])
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                print(f"Error in real-time transcription: {e}")
    
    def add_audio_chunk(self, audio_chunk: np.ndarray):
        """Add audio chunk to processing queue for real-time transcription."""
        if self.is_recording:
            self.audio_queue.put(audio_chunk)
    
    def translate_audio(self, audio_path: str, target_language: str = "en") -> Dict[str, Any]:
        """
        Translate audio to target language.
        
        Args:
            audio_path (str): Path to audio file
            target_language (str): Target language code
            
        Returns:
            dict: Translation result
        """
        print(f"Translating audio to {target_language}...")
        
        result = self.transcribe_with_options(
            audio_path,
            task="translate",
            language=target_language
        )
        
        return result
    
    def get_audio_info(self, audio_path: str) -> Dict[str, Any]:
        """
        Get information about an audio file.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Audio information
        """
        try:
            # Load audio with librosa
            y, sr = librosa.load(audio_path, sr=None)
            
            # Get duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Get basic stats
            info = {
                "file_path": audio_path,
                "sample_rate": sr,
                "duration": duration,
                "channels": 1 if len(y.shape) == 1 else y.shape[1],
                "samples": len(y),
                "file_size": os.path.getsize(audio_path)
            }
            
            return info
            
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return {"error": str(e)}

def main():
    """Main function to demonstrate advanced Whisper features."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Whisper transcription")
    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size")
    parser.add_argument("--device", default=None,
                       choices=["cpu", "cuda", "mps"],
                       help="Device to use")
    parser.add_argument("--task", default="transcribe",
                       choices=["transcribe", "translate"],
                       help="Task to perform")
    parser.add_argument("--language", default=None,
                       help="Language code (auto-detect if not specified)")
    parser.add_argument("--info", action="store_true",
                       help="Show audio file information")
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = AdvancedWhisperTranscriber(
        model_name=args.model,
        device=args.device
    )
    
    # Show audio info if requested
    if args.info:
        info = transcriber.get_audio_info(args.audio_file)
        print("\n📊 Audio Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
    
    # Detect language
    detected_lang = transcriber.detect_language(args.audio_file)
    
    # Transcribe or translate
    try:
        if args.task == "translate":
            result = transcriber.translate_audio(args.audio_file, args.language or "en")
            print(f"\n🌐 Translation completed!")
        else:
            result = transcriber.transcribe_with_options(
                args.audio_file,
                language=args.language or detected_lang
            )
            print(f"\n📝 Transcription completed!")
        
        print(f"Text: {result['text'][:200]}...")
        print(f"Language: {result['language']}")
        print(f"Duration: {result['segments'][-1]['end']:.2f} seconds")
        
        # Save result
        output_path = f"{Path(args.audio_file).stem}_{args.task}.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        print(f"✅ Result saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
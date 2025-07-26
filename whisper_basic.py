#!/usr/bin/env python3
"""
Basic Whisper Implementation
A simple script to transcribe audio files using OpenAI's Whisper model.
"""

import whisper
import os
import sys
from pathlib import Path

class WhisperTranscriber:
    def __init__(self, model_name="base"):
        """
        Initialize Whisper transcriber with specified model.
        
        Args:
            model_name (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model_name = model_name
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the Whisper model."""
        print(f"Loading {self.model_name} model...")
        try:
            self.model = whisper.load_model(self.model_name)
            print(f"✅ {self.model_name} model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)
    
    def transcribe_file(self, audio_path, output_format="txt"):
        """
        Transcribe an audio file to text.
        
        Args:
            audio_path (str): Path to the audio file
            output_format (str): Output format ('txt', 'srt', 'vtt')
            
        Returns:
            dict: Transcription result
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing: {audio_path}")
        
        # Transcribe the audio
        result = self.model.transcribe(audio_path)
        
        # Save transcription
        self._save_transcription(result, audio_path, output_format)
        
        return result
    
    def _save_transcription(self, result, audio_path, output_format):
        """Save transcription to file."""
        base_path = Path(audio_path).stem
        output_path = f"{base_path}_transcription.{output_format}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_format == "txt":
                f.write(result["text"])
            elif output_format == "srt":
                f.write(self._format_srt(result))
            elif output_format == "vtt":
                f.write(self._format_vtt(result))
        
        print(f"✅ Transcription saved to: {output_path}")
    
    def _format_srt(self, result):
        """Format transcription as SRT subtitles."""
        srt_content = ""
        for i, segment in enumerate(result["segments"], 1):
            start_time = self._format_time(segment["start"])
            end_time = self._format_time(segment["end"])
            text = segment["text"].strip()
            
            srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        
        return srt_content
    
    def _format_vtt(self, result):
        """Format transcription as VTT subtitles."""
        vtt_content = "WEBVTT\n\n"
        for segment in result["segments"]:
            start_time = self._format_time(segment["start"], vtt=True)
            end_time = self._format_time(segment["end"], vtt=True)
            text = segment["text"].strip()
            
            vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
        
        return vtt_content
    
    def _format_time(self, seconds, vtt=False):
        """Format seconds to timestamp."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        if vtt:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def main():
    """Main function to demonstrate Whisper usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--output", default="txt",
                       choices=["txt", "srt", "vtt"],
                       help="Output format (default: txt)")
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = WhisperTranscriber(model_name=args.model)
    
    # Transcribe the file
    try:
        result = transcriber.transcribe_file(args.audio_file, args.output)
        print(f"\n📝 Transcription completed!")
        print(f"Text: {result['text'][:200]}...")
        print(f"Language: {result['language']}")
        print(f"Duration: {result['segments'][-1]['end']:.2f} seconds")
    except Exception as e:
        print(f"❌ Error during transcription: {e}")

if __name__ == "__main__":
    main() 
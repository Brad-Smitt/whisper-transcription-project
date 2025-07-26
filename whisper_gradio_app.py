#!/usr/bin/env python3
"""
Application Gradio Whisper
Une application Gradio simple pour la transcription audio utilisant OpenAI's Whisper.
"""

import gradio as gr
import whisper
import tempfile
import os
import json
from pathlib import Path
from typing import Dict, Any

class WhisperGradioApp:
    def __init__(self):
        """Initialiser l'application Gradio."""
        self.model = None
        self.current_model_name = None
    
    def load_model(self, model_name: str):
        """Charger le modèle Whisper."""
        if self.current_model_name != model_name:
            print(f"Chargement du modèle {model_name}...")
            self.model = whisper.load_model(model_name)
            self.current_model_name = model_name
            print(f"✅ Modèle {model_name} chargé !")
        return f"✅ Modèle {model_name} chargé !"
    
    def transcribe_audio(self, audio_file, model_name, task, language, temperature, word_timestamps):
        """Transcrire un fichier audio."""
        try:
            # Charger le modèle si nécessaire
            self.load_model(model_name)
            
            # Préparer les options
            options = {
                "task": task,
                "temperature": temperature,
                "word_timestamps": word_timestamps
            }
            
            if language and language != "Détection automatique":
                # Convertir les noms de langues en codes
                language_codes = {
                    "Français": "fr",
                    "Anglais": "en",
                    "Espagnol": "es",
                    "Allemand": "de",
                    "Italien": "it",
                    "Portugais": "pt",
                    "Russe": "ru",
                    "Japonais": "ja",
                    "Coréen": "ko",
                    "Chinois": "zh"
                }
                options["language"] = language_codes.get(language, language)
            
            # Transcrire
            result = self.model.transcribe(audio_file.name, **options)
            
            # Formater la sortie
            output = {
                "text": result["text"],
                "language": result.get("language", "Inconnue"),
                "segments": len(result.get("segments", [])),
                "duration": result["segments"][-1]["end"] if result.get("segments") else 0
            }
            
            # Créer le texte formaté pour l'affichage
            info_text = f"🌍 Langue détectée : {output['language']}\n"
            info_text += f"📊 Nombre de segments : {output['segments']}\n"
            info_text += f"⏱️ Durée : {output['duration']:.2f} secondes"
            
            return (
                result["text"],
                info_text,
                json.dumps(result, indent=2, ensure_ascii=False)
            )
            
        except Exception as e:
            return f"Erreur : {str(e)}", "", ""
    
    def create_interface(self):
        """Créer l'interface Gradio."""
        
        # Composants de l'interface
        with gr.Blocks(title="Transcription Whisper", theme=gr.themes.Soft()) as interface:
            
            gr.Markdown("# 🎤 Application de Transcription Whisper")
            gr.Markdown("Déposez un fichier audio et obtenez des transcriptions précises avec le modèle Whisper d'OpenAI.")
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Composants d'entrée
                    audio_input = gr.Audio(
                        label="📁 Déposer le Fichier Audio",
                        type="filepath",
                        source="upload"
                    )
                    
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            choices=["tiny", "base", "small", "medium", "large"],
                            value="base",
                            label="🤖 Modèle",
                            info="Les modèles plus grands sont plus précis mais plus lents"
                        )
                        
                        task_dropdown = gr.Dropdown(
                            choices=["transcribe", "translate"],
                            value="transcribe",
                            label="🎯 Tâche",
                            info="Transcrire ou traduire en anglais"
                        )
                    
                    with gr.Row():
                        language_dropdown = gr.Dropdown(
                            choices=["Détection automatique", "Français", "Anglais", "Espagnol", "Allemand", "Italien", "Portugais", "Russe", "Japonais", "Coréen", "Chinois"],
                            value="Détection automatique",
                            label="🌍 Langue",
                            info="Sélectionner la langue ou laisser la détection automatique"
                        )
                        
                        temperature_slider = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.0,
                            step=0.1,
                            label="🌡️ Température",
                            info="Valeurs plus élevées rendent la sortie plus aléatoire"
                        )
                    
                    word_timestamps_checkbox = gr.Checkbox(
                        label="⏱️ Horodatage au niveau des mots",
                        value=False,
                        info="Inclure les horodatages pour chaque mot"
                    )
                    
                    transcribe_button = gr.Button("🎯 Transcrire", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    # Composants de sortie
                    text_output = gr.Textbox(
                        label="📝 Texte Transcrit",
                        lines=10,
                        placeholder="La transcription apparaîtra ici..."
                    )
                    
                    info_output = gr.Textbox(
                        label="ℹ️ Informations",
                        lines=3,
                        placeholder="Informations supplémentaires..."
                    )
                    
                    json_output = gr.Code(
                        label="📊 Résultat JSON Complet",
                        language="json",
                        lines=20
                    )
            
            # Gestionnaires d'événements
            transcribe_button.click(
                fn=self.transcribe_audio,
                inputs=[
                    audio_input,
                    model_dropdown,
                    task_dropdown,
                    language_dropdown,
                    temperature_slider,
                    word_timestamps_checkbox
                ],
                outputs=[text_output, info_output, json_output]
            )
            
            # Exemples
            gr.Examples(
                examples=[
                    ["exemple_audio.wav", "base", "transcribe", "Détection automatique", 0.0, False],
                ],
                inputs=[
                    audio_input,
                    model_dropdown,
                    task_dropdown,
                    language_dropdown,
                    temperature_slider,
                    word_timestamps_checkbox
                ],
                outputs=[text_output, info_output, json_output],
                fn=self.transcribe_audio,
                cache_examples=True
            )
            
            # Pied de page
            gr.Markdown("""
            ---
            ### 📚 Conseils d'Utilisation
            
            - **Modèles Tiny/Base** : Plus rapides mais moins précis
            - **Modèle Large** : Plus précis mais plus lent
            - **Détection automatique** : Fonctionne bien pour la plupart des langues
            - **Horodatage des mots** : Utile pour la création de sous-titres
            - Formats supportés : WAV, MP3, M4A, FLAC, OGG
            
            ### 🔧 Fonctionnalités Avancées
            
            - **Température** : Contrôle la randomisation de la sortie
            - **Sélection de langue** : Peut améliorer la précision pour des langues spécifiques
            - **Traduction** : Traduire automatiquement en anglais
            - **Horodatage des mots** : Obtenir un timing précis pour chaque mot
            """)
        
        return interface

def main():
    """Fonction principale pour lancer l'application Gradio."""
    app = WhisperGradioApp()
    interface = app.create_interface()
    
    # Lancer l'application
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )

if __name__ == "__main__":
    main() 
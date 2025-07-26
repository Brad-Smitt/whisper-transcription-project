#!/usr/bin/env python3
"""
Application Web Whisper
Une application Streamlit pour la transcription audio utilisant OpenAI's Whisper.
"""

import streamlit as st
import whisper
import tempfile
import os
import time
from pathlib import Path
import io
import base64
from typing import Dict, Any

# Configuration de la page
st.set_page_config(
    page_title="Application de Transcription Whisper",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un meilleur style
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .upload-area {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #1f77b4;
        background-color: #e3f2fd;
    }
    .model-button {
        margin: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 2px solid #ddd;
        background-color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .model-button:hover {
        border-color: #1f77b4;
        background-color: #e3f2fd;
    }
    .model-button.selected {
        border-color: #1f77b4;
        background-color: #1f77b4;
        color: white;
    }
    .language-button {
        margin: 0.25rem;
        padding: 0.25rem 0.5rem;
        border-radius: 3px;
        border: 1px solid #ddd;
        background-color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    .language-button:hover {
        border-color: #1f77b4;
        background-color: #e3f2fd;
    }
    .language-button.selected {
        border-color: #1f77b4;
        background-color: #1f77b4;
        color: white;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_whisper_model(model_name: str = "base"):
    """Charger le modèle Whisper avec mise en cache."""
    with st.spinner(f"Chargement du modèle {model_name}..."):
        model = whisper.load_model(model_name)
    return model

def transcribe_audio(model, audio_file, options: Dict[str, Any]) -> Dict[str, Any]:
    """Transcrire un fichier audio avec les options données."""
    try:
        # Sauvegarder le fichier uploadé temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        # Transcrire
        result = model.transcribe(tmp_path, **options)
        
        # Nettoyer
        os.unlink(tmp_path)
        
        return result
    except Exception as e:
        st.error(f"Erreur lors de la transcription : {e}")
        return None

def main():
    """Fonction principale de l'application."""
    
    # En-tête
    st.markdown('<h1 class="main-header">🎤 Application de Transcription Whisper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Déposez vos fichiers audio et obtenez des transcriptions précises avec OpenAI Whisper</p>', unsafe_allow_html=True)
    
    # Configuration de la barre latérale
    st.sidebar.header("⚙️ Configuration")
    
    # Sélection du modèle avec boutons
    st.sidebar.subheader("🤖 Modèle")
    model_options = {
        "tiny": "Tiny (39 MB) - Rapide",
        "base": "Base (74 MB) - Équilibré", 
        "small": "Small (244 MB) - Meilleur",
        "medium": "Medium (769 MB) - Élevé",
        "large": "Large (1550 MB) - Maximum"
    }
    
    selected_model = st.sidebar.selectbox(
        "Choisir le modèle",
        list(model_options.keys()),
        index=1,
        format_func=lambda x: model_options[x],
        help="Les modèles plus grands sont plus précis mais plus lents"
    )
    
    # Sélection de la tâche
    st.sidebar.subheader("🎯 Tâche")
    task = st.sidebar.selectbox(
        "Type de traitement",
        ["transcribe", "translate"],
        format_func=lambda x: "Transcrire" if x == "transcribe" else "Traduire en anglais",
        help="Transcrire dans la langue originale ou traduire en anglais"
    )
    
    # Sélection de la langue avec boutons
    st.sidebar.subheader("🌍 Langue")
    language_options = {
        "Auto-detect": "Détection automatique",
        "fr": "Français",
        "en": "Anglais", 
        "es": "Espagnol",
        "de": "Allemand",
        "it": "Italien",
        "pt": "Portugais",
        "ru": "Russe",
        "ja": "Japonais",
        "ko": "Coréen",
        "zh": "Chinois"
    }
    
    selected_language = st.sidebar.selectbox(
        "Sélectionner la langue",
        list(language_options.keys()),
        format_func=lambda x: language_options[x],
        help="Sélectionner la langue ou laisser la détection automatique"
    )
    
    # Options avancées
    st.sidebar.header("🔧 Options Avancées")
    
    with st.sidebar.expander("Paramètres Avancés"):
        temperature = st.slider("Température", 0.0, 1.0, 0.0, 0.1,
                              help="Valeurs plus élevées rendent la sortie plus aléatoire")
        
        word_timestamps = st.checkbox("Horodatage au niveau des mots", False,
                                    help="Inclure les horodatages pour chaque mot")
        
        initial_prompt = st.text_area("Invite initiale", "",
                                     help="Fournir du contexte pour améliorer la transcription")
    
    # Charger le modèle
    model = load_whisper_model(selected_model)
    
    # Zone principale de contenu
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Déposer le Fichier Audio")
        
        # Zone de dépôt de fichier stylisée
        st.markdown("""
        <div class="upload-area">
            <h3>🎵 Glissez-déposez votre fichier audio ici</h3>
            <p>ou cliquez pour sélectionner un fichier</p>
            <p><small>Formats supportés : WAV, MP3, M4A, FLAC, OGG</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "Choisir un fichier audio",
            type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
            help="Formats supportés : WAV, MP3, M4A, FLAC, OGG",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Afficher les informations du fichier
            file_details = {
                "Nom du fichier": uploaded_file.name,
                "Taille du fichier": f"{uploaded_file.size / 1024:.1f} KB",
                "Type de fichier": uploaded_file.type
            }
            
            st.success("📊 Informations du Fichier")
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
            
            # Options de transcription
            options = {
                "task": task,
                "temperature": temperature,
                "word_timestamps": word_timestamps,
                "initial_prompt": initial_prompt if initial_prompt else None
            }
            
            if selected_language != "Auto-detect":
                options["language"] = selected_language
            
            # Bouton de transcription
            if st.button("🎯 Commencer la Transcription", type="primary"):
                with st.spinner("Transcription en cours..."):
                    result = transcribe_audio(model, uploaded_file, options)
                
                if result:
                    st.success("✅ Transcription terminée !")
                    
                    # Afficher les résultats
                    st.header("📝 Résultats de la Transcription")
                    
                    # Texte principal
                    st.subheader("Texte Transcrit")
                    st.text_area("Texte", result["text"], height=200)
                    
                    # Informations sur la langue
                    if "language" in result:
                        st.info(f"🌍 Langue détectée : {result['language']}")
                    
                    # Segments avec horodatages
                    if "segments" in result and result["segments"]:
                        st.subheader("⏱️ Horodatages")
                        
                        segments_text = ""
                        for i, segment in enumerate(result["segments"], 1):
                            start = f"{segment['start']:.2f}"
                            end = f"{segment['end']:.2f}"
                            text = segment["text"].strip()
                            segments_text += f"{i}. [{start}s - {end}s] {text}\n\n"
                        
                        st.text_area("Segments", segments_text, height=300)
                    
                    # Options de téléchargement
                    st.subheader("💾 Télécharger les Résultats")
                    
                    col_d1, col_d2, col_d3 = st.columns(3)
                    
                    with col_d1:
                        # Télécharger en texte
                        st.download_button(
                            label="📄 Télécharger en TXT",
                            data=result["text"],
                            file_name=f"{Path(uploaded_file.name).stem}_transcription.txt",
                            mime="text/plain"
                        )
                    
                    with col_d2:
                        # Télécharger en SRT
                        if "segments" in result:
                            srt_content = ""
                            for i, segment in enumerate(result["segments"], 1):
                                start_time = format_time(segment["start"])
                                end_time = format_time(segment["end"])
                                text = segment["text"].strip()
                                srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
                            
                            st.download_button(
                                label="🎬 Télécharger en SRT",
                                data=srt_content,
                                file_name=f"{Path(uploaded_file.name).stem}_transcription.srt",
                                mime="text/plain"
                            )
                    
                    with col_d3:
                        # Télécharger en JSON
                        import json
                        st.download_button(
                            label="📊 Télécharger en JSON",
                            data=json.dumps(result, indent=2, ensure_ascii=False),
                            file_name=f"{Path(uploaded_file.name).stem}_transcription.json",
                            mime="application/json"
                        )
    
    with col2:
        st.header("ℹ️ Informations")
        
        # Informations sur le modèle
        st.info("🤖 Informations du Modèle")
        st.write(f"**Modèle :** {selected_model}")
        st.write(f"**Tâche :** {'Transcription' if task == 'transcribe' else 'Traduction'}")
        st.write(f"**Langue :** {language_options[selected_language]}")
        
        # Conseils d'utilisation
        st.info("💡 Conseils d'Utilisation")
        st.write("""
        • **Modèles Tiny/Base** : Plus rapides mais moins précis
        • **Modèle Large** : Plus précis mais plus lent
        • **Détection automatique** : Fonctionne bien pour la plupart des langues
        • **Invite initiale** : Peut améliorer la précision pour des sujets spécifiques
        • **Horodatage des mots** : Utile pour la création de sous-titres
        """)
        
        # Formats supportés
        st.info("🎵 Formats Supportés")
        st.write("""
        • WAV, MP3, M4A
        • FLAC, OGG
        • La plupart des formats audio courants
        """)
        
        # Statut du modèle
        st.info("📊 Statut")
        st.write(f"✅ Modèle {selected_model} chargé")
        st.write("🟢 Prêt pour la transcription")

def format_time(seconds):
    """Formater les secondes en timestamp SRT."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

if __name__ == "__main__":
    main() 
# 🎤 Projet de Transcription Whisper

Une implémentation complète du modèle de reconnaissance vocale Whisper d'OpenAI avec interfaces web modernes, ergonomiques et localisées en français.

## ✨ Nouveautés de l'Interface Web

- **Dépôt de fichier moderne** : Glissez-déposez ou cliquez pour sélectionner un fichier audio (WAV, MP3, M4A, FLAC, OGG)
- **Sélection du modèle** : Choisissez entre Tiny, Base, Small, Medium, Large (avec descriptions)
- **Sélection de la langue** : Français, Anglais, Espagnol, etc. ou détection automatique
- **Interface 100% française** : Tous les textes, boutons et messages sont en français
- **Options avancées** : Température, horodatage des mots, invite initiale
- **Téléchargement des résultats** : TXT, SRT, JSON
- **Design responsive** : Utilisable sur ordinateur et mobile

## 🚀 Démarrage Rapide

### Installation

1. **Téléchargez ou clonez les fichiers du projet**
2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Installez FFmpeg** (requis pour le traitement audio) :
   - **macOS** : `brew install ffmpeg`
   - **Ubuntu/Debian** : `sudo apt install ffmpeg`
   - **Windows** : Téléchargez depuis le [site FFmpeg](https://ffmpeg.org/download.html)

### Application Web (Recommandé)

#### Application Streamlit (interface française, dépôt de fichier, sélection modèle/langue)
```bash
streamlit run whisper_web_app.py
```
- **Fonctionnalités :**
  - Dépôt de fichier par glisser-déposer ou clic
  - Sélection du modèle (Tiny, Base, Small, Medium, Large)
  - Sélection de la langue (français, anglais, espagnol, etc. ou auto)
  - Options avancées : température, horodatage, invite initiale
  - Téléchargement TXT, SRT, JSON
  - Interface 100% en français

#### Application Gradio (interface française, dépôt de fichier, sélection modèle/langue)
```bash
python whisper_gradio_app.py
```
- **Fonctionnalités :**
  - Dépôt de fichier par glisser-déposer ou clic
  - Sélection du modèle et de la langue (libellés en français)
  - Résultats téléchargeables et affichage JSON

### Utilisation en Ligne de Commande

```bash
# Transcription basique
python whisper_basic.py fichier_audio.wav

# Avec modèle spécifique et format de sortie
python whisper_basic.py fichier_audio.wav --model large --output srt

# Fonctionnalités avancées
python whisper_advanced.py fichier_audio.wav --model medium --task translate --info
```

## 📁 Structure des Fichiers

```
whisper_project/
├── requirements.txt          # Dépendances Python
├── whisper_basic.py         # Interface en ligne de commande basique
├── whisper_advanced.py      # Fonctionnalités avancées
├── whisper_web_app.py       # Application web Streamlit (interface moderne FR)
├── whisper_gradio_app.py    # Application web Gradio (interface moderne FR)
├── example_usage.py         # Exemples d'utilisation
├── install.sh               # Script d'installation automatique
├── install_fr.sh            # Script d'installation en français
├── README.md                # Documentation anglaise
└── README_FR.md             # Documentation française
```

## 🖥️ Points Forts de l'Interface Web

- **Dépôt de fichier moderne** : Glissez-déposez ou cliquez pour sélectionner
- **Sélection du modèle** : Tiny, Base, Small, Medium, Large (avec descriptions)
- **Sélection de la langue** : Français, Anglais, Espagnol, etc. ou détection automatique
- **Interface 100% française** : Expérience utilisateur fluide
- **Téléchargement des résultats** : TXT, SRT, JSON
- **Design responsive** : Adapté à tous les écrans

## 🌍 Langues Supportées

Whisper supporte 99+ langues dont :
- Français (fr)
- Anglais (en)
- Espagnol (es)
- Allemand (de)
- Italien (it)
- Portugais (pt)
- Russe (ru)
- Japonais (ja)
- Coréen (ko)
- Chinois (zh)
- Et bien d'autres...

## 📝 Licence

Ce projet utilise le modèle Whisper d'OpenAI. Veuillez vous référer aux termes de licence d'OpenAI.

---

**Bonne transcription ! 🎤✨** 
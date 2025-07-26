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

#### Option 1 : Installation Automatisée (Recommandé)
```bash
# Installation en anglais
./install.sh

# Installation en français
./install_fr.sh
```

#### Option 2 : Installation Manuelle
1. **Cloner le dépôt** :
   ```bash
   git clone <url-de-votre-repo>
   cd whisper_project
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Installer FFmpeg** (requis pour le traitement audio) :
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

# Exécuter les exemples
python example_usage.py
```

## 📁 Structure du Projet

```
whisper_project/
├── 📄 README.md                # Documentation anglaise
├── 📄 README_FR.md             # Documentation française
├── 📄 requirements.txt         # Dépendances Python
├── 📄 LICENSE                  # Licence MIT
├── 📄 .gitignore              # Règles Git ignore
├── 🐍 whisper_basic.py        # Interface en ligne de commande basique
├── 🐍 whisper_advanced.py     # Fonctionnalités avancées
├── 🐍 whisper_web_app.py      # Application web Streamlit (interface moderne FR)
├── 🐍 whisper_gradio_app.py   # Application web Gradio (interface moderne FR)
├── 🐍 example_usage.py        # Exemples d'utilisation
├── 🔧 install.sh              # Script d'installation automatique (anglais)
└── 🔧 install_fr.sh           # Script d'installation automatique (français)
```

## 🖥️ Points Forts de l'Interface Web

- **Dépôt de fichier moderne** : Glissez-déposez ou cliquez pour sélectionner
- **Sélection du modèle** : Tiny, Base, Small, Medium, Large (avec descriptions)
- **Sélection de la langue** : Français, Anglais, Espagnol, etc. ou détection automatique
- **Interface 100% française** : Expérience utilisateur fluide
- **Téléchargement des résultats** : TXT, SRT, JSON
- **Design responsive** : Adapté à tous les écrans

## 🎛️ Options de Modèles

| Modèle | Taille | Vitesse | Précision | Cas d'Usage |
|--------|--------|--------------|---------------|-------------|
| tiny   | 39 MB  | Plus rapide | Plus faible | Tests rapides, ressources limitées |
| base   | 74 MB  | Rapide | Bonne | Usage général |
| small  | 244 MB | Moyenne | Meilleure | Précision améliorée nécessaire |
| medium | 769 MB | Lente | Élevée | Précision élevée requise |
| large  | 1550 MB| Plus lente | Meilleure | Précision maximale, usage professionnel |

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

## 📊 Formats de Sortie

### Texte (TXT)
Sortie texte simple de la transcription.

### SRT (SubRip)
Format de sous-titres avec horodatage pour l'édition vidéo.

### VTT (WebVTT)
Format de pistes texte pour applications web.

### JSON
Données complètes de transcription avec métadonnées et horodatages.

## 🔧 Configuration Avancée

### Options en Ligne de Commande

**Script Basique** :
- `--model` : Taille du modèle (tiny, base, small, medium, large)
- `--output` : Format de sortie (txt, srt, vtt)

**Script Avancé** :
- `--model` : Taille du modèle
- `--device` : Périphérique (cpu, cuda, mps)
- `--task` : Type de tâche (transcribe, translate)
- `--language` : Code de langue
- `--info` : Afficher les informations du fichier audio

## 🐛 Dépannage

### Problèmes Courants

1. **FFmpeg non trouvé** :
   ```bash
   # Installer FFmpeg
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Ubuntu
   ```

2. **Mémoire CUDA insuffisante** :
   - Utilisez un modèle plus petit (tiny, base)
   - Utilisez CPU au lieu de GPU
   - Traitez des fichiers audio plus courts

3. **Transcription lente** :
   - Utilisez des modèles plus petits pour un traitement plus rapide
   - Utilisez l'accélération GPU si disponible
   - Considérez le traitement par lot pour plusieurs fichiers

4. **Précision médiocre** :
   - Utilisez des modèles plus grands (medium, large)
   - Fournissez des invites initiales pour le contexte
   - Assurez-vous d'une bonne qualité audio

## 🤝 Contribution

1. Forkez le dépôt
2. Créez une branche de fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajouter une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

**Note** : Ce projet utilise le modèle Whisper d'OpenAI. Veuillez vous référer aux termes de licence d'OpenAI pour le modèle Whisper lui-même.

## 📚 Ressources Supplémentaires

- [Article Whisper OpenAI](https://arxiv.org/abs/2212.04356)
- [Dépôt GitHub Whisper](https://github.com/openai/whisper)
- [Documentation FFmpeg](https://ffmpeg.org/documentation.html)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Gradio](https://gradio.app/docs/)

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez la section de dépannage ci-dessus
2. Assurez-vous que toutes les dépendances sont installées
3. Vérifiez que FFmpeg est correctement installé
4. Vérifiez la compatibilité du format de fichier audio
5. Ouvrez un issue sur GitHub avec des informations détaillées

---

**Bonne transcription ! 🎤✨** 
#!/bin/bash

# Script d'Installation du Projet Whisper
# Ce script aide à configurer le projet de transcription Whisper

echo "🎤 Script d'Installation du Projet Whisper"
echo "=========================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez installer Python 3.8 ou supérieur."
    exit 1
fi

echo "✅ Python 3 trouvé : $(python3 --version)"

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez installer pip."
    exit 1
fi

echo "✅ pip3 trouvé : $(pip3 --version)"

# Vérifier si FFmpeg est installé
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg n'est pas installé. Ceci est requis pour le traitement audio."
    echo "Installation de FFmpeg..."
    
    # Détecter l'OS et installer FFmpeg
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Homebrew non trouvé. Veuillez installer Homebrew d'abord :"
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
            echo "❌ Gestionnaire de paquets non trouvé. Veuillez installer FFmpeg manuellement."
            exit 1
        fi
    else
        echo "❌ OS non supporté. Veuillez installer FFmpeg manuellement."
        exit 1
    fi
else
    echo "✅ FFmpeg trouvé : $(ffmpeg -version | head -n1)"
fi

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv whisper_env

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source whisper_env/bin/activate

# Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📚 Installation des dépendances Python..."
pip install -r requirements.txt

# Tester l'installation
echo "🧪 Test de l'installation..."
python3 -c "import whisper; print('✅ Whisper importé avec succès')" 2>/dev/null || {
    echo "❌ L'installation de Whisper a échoué. Veuillez vérifier les messages d'erreur ci-dessus."
    exit 1
}

echo ""
echo "🎉 Installation terminée avec succès !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Activer l'environnement virtuel :"
echo "   source whisper_env/bin/activate"
echo ""
echo "2. Exécuter le script d'exemples :"
echo "   python example_usage.py"
echo ""
echo "3. Utiliser le transcripteur basique :"
echo "   python whisper_basic.py votre_fichier_audio.wav"
echo ""
echo "4. Lancer les applications web :"
echo "   streamlit run whisper_web_app.py"
echo "   python whisper_gradio_app.py"
echo ""
echo "📖 Pour plus d'informations, consultez README_FR.md"
echo ""
echo "Bonne transcription ! 🎤✨" 
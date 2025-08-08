# iDoctor-CR — Assistant de préparation de comptes rendus (MVP)

Cette application MVP permet de:
- Planifier des rendez-vous (patient, médecin, date/heure, notes)
- Enregistrer ou téléverser un fichier audio lié à un rendez-vous
- Lancer une transcription factice (stub) côté serveur
- Générer un CR factice (résumé) à partir de la transcription
- Visualiser transcription et CR pour relecture par les secrétaires

Le tout est livré avec:
- Backend: FastAPI + SQLite (SQLModel)
- Frontend léger statique (HTML/JS) servi par le backend

Avertissement: la transcription et le résumé sont des stubs par défaut. Vous pouvez brancher un moteur de STT (ex: Whisper/faster-whisper) et un modèle de résumé (LLM) par la suite.

## Démarrage rapide

Prérequis:
- Python 3.10+

Installation et lancement:

```bash
cd /workspace/idoctor-cr
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Puis ouvrez le frontend:
- Naviguez sur `http://localhost:8000/`
- La documentation API est accessible sur `http://localhost:8000/docs`

Les données (SQLite) sont stockées dans `data/app.db`. Les fichiers transférés sont dans `storage/uploads/`.

## Personnalisation transcription

Le service actuel `app/services/transcription.py` fournit une implémentation factice. Pour une transcription réelle:
- Installez et intégrez un moteur tel que whisper, faster-whisper, vosk, etc.
- Remplacez la fonction `transcribe_recording` pour produire un texte réel.

## Personnalisation génération de CR

Le service actuel `app/services/report.py` génère un gabarit basique à partir de la transcription. Remplacez `generate_report_from_transcription` avec votre logique (règles internes ou appel LLM).

## Structure du projet

```
idoctor-cr/
  app/
    main.py
    database.py
    models.py
    services/
      transcription.py
      report.py
  frontend/
    index.html
    app.js
    styles.css
  data/
  storage/
    uploads/
  requirements.txt
  README.md
```

## Sécurité et conformité

- Ce MVP n’intègre pas d’authentification ni de chiffrement au repos. Pour un usage réel (santé), ajoutez:
  - Authentification/autorisation (OAuth2/OIDC, RBAC)
  - Chiffrement au repos et en transit (HTTPS, gestion des clés)
  - Journalisation/Audit, rétention et purge
  - Hébergement et conformité réglementaire (ex: RGPD)

## Licence

MVP fourni à des fins de démonstration. À adapter selon vos contraintes internes.
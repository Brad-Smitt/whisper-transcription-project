from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import select

from ..models import Recording, Schedule, ScheduleStatus, Transcription, TranscriptionStatus


def transcribe_recording(session, schedule_id: int, recording_id: int) -> None:
    transcription = Transcription(
        schedule_id=schedule_id,
        recording_id=recording_id,
        status=TranscriptionStatus.PENDING,
        text=None,
    )
    session.add(transcription)
    session.commit()
    session.refresh(transcription)

    # STUB: Ici, placez votre logique de STT réelle (whisper, faster-whisper, etc.)
    # Pour le MVP, nous simulons une transcription simple.
    placeholder = (
        "Patient reçu pour consultation. Motif: contrôle de suivi. "
        "Antécédents sans particularité récente. Examen clinique RAS. "
        "Conduite: poursuite du traitement habituel et bilan biologique de routine."
    )

    transcription.text = placeholder
    transcription.status = TranscriptionStatus.COMPLETED
    transcription.updated_at = datetime.now(timezone.utc)
    session.add(transcription)

    # Mettre à jour le statut du rendez-vous
    schedule = session.exec(select(Schedule).where(Schedule.id == schedule_id)).first()
    if schedule:
        schedule.status = ScheduleStatus.TRANSCRIBED
        session.add(schedule)

    session.commit()
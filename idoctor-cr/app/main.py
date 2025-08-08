from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import SQLModel, select

from .database import BASE_DIR, init_db, get_session
from .models import (
    Recording,
    Report,
    ReportStatus,
    Schedule,
    ScheduleStatus,
    Transcription,
    TranscriptionStatus,
)
from .services.transcription import transcribe_recording
from .services.report import generate_report_from_transcription


app = FastAPI(title="iDoctor-CR (MVP)")

# CORS (facultatif pour le même domaine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
FRONTEND_DIR = BASE_DIR / "frontend"


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# Servir les fichiers statiques sous /static et la page d'accueil via /
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR), html=False), name="static")


@app.get("/")
def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="Frontend manquant")
    return FileResponse(str(index_path))


# Schemas Pydantic pour entrées/sorties
class ScheduleCreate(BaseModel):
    patient_name: str
    patient_identifier: Optional[str] = None
    doctor_name: str
    scheduled_at: datetime
    notes: Optional[str] = None


class ScheduleRead(BaseModel):
    id: int
    patient_name: str
    patient_identifier: Optional[str]
    doctor_name: str
    scheduled_at: datetime
    notes: Optional[str]
    status: ScheduleStatus

    class Config:
        from_attributes = True


@app.get("/api/schedules", response_model=List[ScheduleRead])
def list_schedules() -> List[ScheduleRead]:
    with get_session() as session:
        schedules = session.exec(select(Schedule).order_by(Schedule.scheduled_at.desc())).all()
        return schedules


@app.post("/api/schedules", response_model=ScheduleRead)
def create_schedule(payload: ScheduleCreate) -> ScheduleRead:
    schedule = Schedule(**payload.model_dump())
    with get_session() as session:
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule


@app.get("/api/schedules/{schedule_id}", response_model=ScheduleRead)
def get_schedule(schedule_id: int) -> ScheduleRead:
    with get_session() as session:
        obj = session.exec(select(Schedule).where(Schedule.id == schedule_id)).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Rendez-vous introuvable")
        return obj


@app.post("/api/schedules/{schedule_id}/upload")
async def upload_recording(
    schedule_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    media_type: str = "audio",
):
    # Vérifier le rendez-vous
    with get_session() as session:
        schedule = session.exec(select(Schedule).where(Schedule.id == schedule_id)).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="Rendez-vous introuvable")

    # Sauvegarder le fichier
    suffix = Path(file.filename).suffix or (".webm" if media_type == "video" else ".wav")
    unique_name = f"{uuid.uuid4().hex}{suffix}"
    dest_path = UPLOADS_DIR / unique_name

    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Créer enregistrement en DB
    with get_session() as session:
        recording = Recording(
            schedule_id=schedule_id,
            file_path=str(dest_path),
            media_type=media_type,
        )
        session.add(recording)

        # Marquer le rendez-vous comme "recorded"
        schedule = session.exec(select(Schedule).where(Schedule.id == schedule_id)).first()
        if schedule:
            schedule.status = ScheduleStatus.RECORDED
            session.add(schedule)
        session.commit()
        session.refresh(recording)

        # Lancer la transcription en tâche de fond
        background_tasks.add_task(_bg_transcribe, schedule_id, recording.id)

    return {"message": "Fichier reçu", "recording_id": recording.id}


def _bg_transcribe(schedule_id: int, recording_id: int) -> None:
    with get_session() as session:
        transcribe_recording(session, schedule_id=schedule_id, recording_id=recording_id)


@app.get("/api/transcriptions/{schedule_id}")
def get_transcription(schedule_id: int):
    with get_session() as session:
        t = session.exec(
            select(Transcription)
            .where(Transcription.schedule_id == schedule_id)
            .order_by(Transcription.created_at.desc())
        ).first()
        if not t:
            raise HTTPException(status_code=404, detail="Transcription introuvable")
        return {
            "id": t.id,
            "schedule_id": t.schedule_id,
            "status": t.status,
            "text": t.text,
            "updated_at": t.updated_at,
        }


@app.post("/api/schedules/{schedule_id}/generate_report")
def post_generate_report(schedule_id: int, background_tasks: BackgroundTasks):
    # Lancer la génération de CR en arrière-plan
    background_tasks.add_task(_bg_generate_report, schedule_id)
    return {"message": "Génération du CR déclenchée"}


def _bg_generate_report(schedule_id: int) -> None:
    with get_session() as session:
        generate_report_from_transcription(session, schedule_id)


@app.get("/api/reports/{schedule_id}")
def get_report(schedule_id: int):
    with get_session() as session:
        report = session.exec(select(Report).where(Report.schedule_id == schedule_id)).first()
        if not report:
            raise HTTPException(status_code=404, detail="CR introuvable")
        return {
            "id": report.id,
            "schedule_id": report.schedule_id,
            "status": report.status,
            "text": report.text,
            "updated_at": report.updated_at,
        }
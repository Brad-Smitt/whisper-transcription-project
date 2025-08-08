from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class ScheduleStatus(str, Enum):
    PLANNED = "planned"
    RECORDED = "recorded"
    TRANSCRIBED = "transcribed"
    REPORTED = "reported"


class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_name: str
    patient_identifier: Optional[str] = None
    doctor_name: str
    scheduled_at: datetime
    notes: Optional[str] = None
    status: ScheduleStatus = Field(default=ScheduleStatus.PLANNED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Recording(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedule.id")
    file_path: str
    media_type: str = Field(default="audio")  # "audio" ou "video"
    duration_seconds: Optional[float] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TranscriptionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transcription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedule.id")
    recording_id: Optional[int] = Field(default=None, foreign_key="recording.id")
    text: Optional[str] = None
    status: TranscriptionStatus = Field(default=TranscriptionStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReportStatus(str, Enum):
    DRAFT = "draft"
    FINAL = "final"


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedule.id")
    text: Optional[str] = None
    status: ReportStatus = Field(default=ReportStatus.DRAFT)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
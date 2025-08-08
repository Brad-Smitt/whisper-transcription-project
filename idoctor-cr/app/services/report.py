from __future__ import annotations

from datetime import datetime

from sqlmodel import select

from ..models import Report, ReportStatus, Schedule, ScheduleStatus, Transcription


def _build_report_text(schedule: Schedule, transcription_text: str) -> str:
    dt = schedule.scheduled_at.strftime("%d/%m/%Y %H:%M") if schedule.scheduled_at else ""
    header = (
        f"Compte rendu de consultation\n"
        f"Patient: {schedule.patient_name} ({schedule.patient_identifier or 'N/A'})\n"
        f"Médecin: {schedule.doctor_name}\n"
        f"Date/Heure: {dt}\n\n"
    )

    # Découpage naïf en sections
    motif = "Motif de consultation: "
    histoire = "Histoire/Messages clés: "
    examen = "Examen clinique: "
    conclusion = "Conclusion/Conduite: "

    body = (
        f"{motif}{transcription_text[:180]}...\n\n"
        f"{histoire}{transcription_text}\n\n"
        f"{examen}RAS si non précisé.\n\n"
        f"{conclusion}Poursuite du traitement si indiqué.\n"
    )

    return header + body


def generate_report_from_transcription(session, schedule_id: int) -> None:
    schedule = session.exec(select(Schedule).where(Schedule.id == schedule_id)).first()
    if not schedule:
        return

    transcription = session.exec(
        select(Transcription)
        .where(Transcription.schedule_id == schedule_id)
        .order_by(Transcription.created_at.desc())
    ).first()

    if not transcription or not transcription.text:
        # Pas de transcription exploitable
        text = _build_report_text(schedule, "Transcription indisponible.")
    else:
        text = _build_report_text(schedule, transcription.text)

    report = session.exec(select(Report).where(Report.schedule_id == schedule_id)).first()
    if not report:
        report = Report(schedule_id=schedule_id, text=text, status=ReportStatus.DRAFT)
    else:
        report.text = text
        report.status = ReportStatus.DRAFT

    session.add(report)

    # Mettre à jour le statut du rendez-vous
    schedule.status = ScheduleStatus.REPORTED
    session.add(schedule)

    session.commit()
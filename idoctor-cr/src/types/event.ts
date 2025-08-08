export type RecordingKind = "audio" | "video";

export interface ScheduledEvent {
  id: string;
  title: string;
  patientName: string;
  notes?: string;
  startIso: string; // ISO 8601
  endIso?: string;  // ISO 8601
  recordingKind: RecordingKind;
  recordingFileUrl?: string; // /uploads/...
  transcript?: string;
  summary?: string; // Compte rendu
  createdAtIso: string;
  updatedAtIso: string;
}
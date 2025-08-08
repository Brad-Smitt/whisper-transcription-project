"use client";

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ScheduledEvent } from "@/types/event";

export const dynamic = "force-dynamic";

async function getEvent(eventId: string): Promise<ScheduledEvent | null> {
  const res = await fetch("/api/events", { cache: "no-store" });
  const data = await res.json();
  const ev = (data.events as ScheduledEvent[]).find((e) => e.id === eventId);
  return ev ?? null;
}

function RecordInner() {
  const params = useSearchParams();
  const eventId = params.get("eventId");

  const [event, setEvent] = useState<ScheduledEvent | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [chunks, setChunks] = useState<Blob[]>([]);
  const [recording, setRecording] = useState(false);
  const [recordedUrl, setRecordedUrl] = useState<string | null>(null);
  const [uploadUrl, setUploadUrl] = useState<string | null>(null);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (!eventId) return;
    getEvent(eventId).then(setEvent);
  }, [eventId]);

  const start = useCallback(async () => {
    if (!event) return;
    const isVideo = event.recordingKind === "video";
    const media = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: isVideo ? { width: 1280, height: 720 } : false,
    });
    setStream(media);

    const mr = new MediaRecorder(media);
    const localChunks: Blob[] = [];
    mr.ondataavailable = (e) => {
      if (e.data.size > 0) localChunks.push(e.data);
    };
    mr.onstop = () => {
      setChunks(localChunks);
      const blob = new Blob(localChunks, { type: mr.mimeType });
      const url = URL.createObjectURL(blob);
      setRecordedUrl(url);
    };
    setMediaRecorder(mr);

    if (videoRef.current && isVideo) {
      videoRef.current.srcObject = media;
      videoRef.current.muted = true;
      await videoRef.current.play();
    }

    mr.start();
    setRecording(true);
  }, [event]);

  const stop = useCallback(() => {
    mediaRecorder?.stop();
    stream?.getTracks().forEach((t) => t.stop());
    setRecording(false);
  }, [mediaRecorder, stream]);

  const upload = useCallback(async () => {
    if (!chunks.length) return;
    const blob = new Blob(chunks, { type: mediaRecorder?.mimeType || "video/webm" });
    const file = new File([blob], `record-${Date.now()}.webm`);
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch("/api/upload", { method: "POST", body: fd });
    const data = await res.json();
    setUploadUrl(data.url);
  }, [chunks, mediaRecorder]);

  const transcribe = useCallback(async () => {
    if (!uploadUrl || !event) return;
    const res = await fetch("/api/transcribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fileUrl: uploadUrl, language: "fr" }),
    });
    const data = await res.json();
    setTranscript(data.transcript ?? "");
  }, [uploadUrl, event]);

  const summarize = useCallback(async () => {
    if (!transcript || !event) return;
    const res = await fetch("/api/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript, patientName: event.patientName, title: event.title }),
    });
    const data = await res.json();
    setSummary(data.summary ?? "");
  }, [transcript, event]);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Enregistrement</h1>
      {event ? (
        <div className="text-sm text-gray-700">{event.title} — {event.patientName}</div>
      ) : (
        <div className="text-sm text-gray-500">Aucun événement</div>
      )}

      {event?.recordingKind === "video" ? (
        <video ref={videoRef} className="w-full rounded border bg-black" />
      ) : (
        <div className="text-sm text-gray-500">Mode audio</div>
      )}

      <div className="flex gap-2">
        {!recording ? (
          <button className="bg-green-600 text-white rounded px-4 py-2" onClick={start} disabled={!event}>Démarrer</button>
        ) : (
          <button className="bg-red-600 text-white rounded px-4 py-2" onClick={stop}>Arrêter</button>
        )}
        <button className="border rounded px-4 py-2" onClick={upload} disabled={!recordedUrl}>Uploader</button>
        <button className="border rounded px-4 py-2" onClick={transcribe} disabled={!uploadUrl}>Transcrire</button>
        <button className="border rounded px-4 py-2" onClick={summarize} disabled={!transcript}>Résumer</button>
      </div>

      {recordedUrl && (
        <div className="text-sm">Fichier local: <a className="underline" href={recordedUrl} target="_blank">ouvrir</a></div>
      )}
      {uploadUrl && (
        <div className="text-sm">Upload: <a className="underline" href={uploadUrl} target="_blank">{uploadUrl}</a></div>
      )}

      {transcript && (
        <div className="mt-4">
          <h2 className="font-medium">Transcription</h2>
          <pre className="whitespace-pre-wrap text-sm p-3 bg-gray-50 border rounded">{transcript}</pre>
        </div>
      )}

      {summary && (
        <div className="mt-4">
          <h2 className="font-medium">Compte rendu</h2>
          <pre className="whitespace-pre-wrap text-sm p-3 bg-gray-50 border rounded">{summary}</pre>
        </div>
      )}
    </div>
  );
}

export default function RecordPage() {
  return (
    <Suspense>
      <RecordInner />
    </Suspense>
  );
}
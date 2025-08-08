"use client";

import { useEffect, useMemo, useState } from "react";
import { RecordingKind, ScheduledEvent } from "@/types/event";

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

async function fetchEvents(): Promise<ScheduledEvent[]> {
  const res = await fetch("/api/events", { cache: "no-store" });
  const data = await res.json();
  return data.events ?? [];
}

async function saveEvent(event: ScheduledEvent): Promise<ScheduledEvent> {
  const res = await fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  const data = await res.json();
  return data.event;
}

async function deleteEventById(id: string): Promise<void> {
  await fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ deleteId: id }),
  });
}

export default function AgendaPage() {
  const [events, setEvents] = useState<ScheduledEvent[] | null>(null);
  const [form, setForm] = useState({
    title: "Consultation",
    patientName: "",
    startIso: new Date().toISOString().slice(0, 16),
    endIso: "",
    notes: "",
    recordingKind: "audio" as RecordingKind,
  });

  useEffect(() => {
    fetchEvents().then(setEvents);
  }, []);

  const sorted = useMemo(() =>
    (events ?? []).slice().sort((a, b) => a.startIso.localeCompare(b.startIso)), [events]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const event: ScheduledEvent = {
      id: generateId(),
      title: form.title || "Consultation",
      patientName: form.patientName || "",
      notes: form.notes || "",
      startIso: new Date(form.startIso).toISOString(),
      endIso: form.endIso ? new Date(form.endIso).toISOString() : undefined,
      recordingKind: form.recordingKind,
      createdAtIso: new Date().toISOString(),
      updatedAtIso: new Date().toISOString(),
    };
    const saved = await saveEvent(event);
    setEvents((prev) => [ ...(prev ?? []), saved ]);
  }

  async function handleDelete(id: string) {
    await deleteEventById(id);
    setEvents((prev) => (prev ?? []).filter((e) => e.id !== id));
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Agenda</h1>

      <form className="grid grid-cols-1 gap-3" onSubmit={handleSubmit}>
        <div className="grid sm:grid-cols-2 gap-3">
          <input className="border rounded px-3 py-2" placeholder="Titre" value={form.title}
                 onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))} />
          <input className="border rounded px-3 py-2" placeholder="Patient" value={form.patientName}
                 onChange={(e) => setForm((f) => ({ ...f, patientName: e.target.value }))} />
        </div>
        <div className="grid sm:grid-cols-2 gap-3">
          <input type="datetime-local" className="border rounded px-3 py-2" value={form.startIso}
                 onChange={(e) => setForm((f) => ({ ...f, startIso: e.target.value }))} />
          <input type="datetime-local" className="border rounded px-3 py-2" value={form.endIso}
                 onChange={(e) => setForm((f) => ({ ...f, endIso: e.target.value }))} />
        </div>
        <div className="grid sm:grid-cols-2 gap-3 items-center">
          <select className="border rounded px-3 py-2" value={form.recordingKind}
                  onChange={(e) => setForm((f) => ({ ...f, recordingKind: e.target.value as RecordingKind }))}>
            <option value="audio">Audio</option>
            <option value="video">Vidéo</option>
          </select>
          <input className="border rounded px-3 py-2" placeholder="Notes" value={form.notes}
                 onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))} />
        </div>
        <button type="submit" className="bg-black text-white rounded px-4 py-2 w-fit">Ajouter</button>
      </form>

      <div className="divide-y border rounded">
        {sorted.map((ev) => (
          <div key={ev.id} className="p-4 flex items-start gap-3">
            <div className="flex-1">
              <div className="font-medium">{ev.title} — {ev.patientName}</div>
              <div className="text-sm text-gray-500">
                {new Date(ev.startIso).toLocaleString()} {ev.endIso ? `→ ${new Date(ev.endIso).toLocaleString()}` : ""}
              </div>
              {ev.notes ? <div className="text-sm mt-1">{ev.notes}</div> : null}
            </div>
            <a href={`/enregistrement?eventId=${ev.id}`} className="text-blue-600 underline">Enregistrer</a>
            <button onClick={() => handleDelete(ev.id)} className="text-red-600">Supprimer</button>
          </div>
        ))}
        {sorted.length === 0 && (
          <div className="p-4 text-sm text-gray-500">Aucun événement</div>
        )}
      </div>
    </div>
  );
}
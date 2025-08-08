import { NextRequest } from "next/server";
import { readAllEvents, upsertEvent, deleteEvent } from "@/lib/storage";
import { ScheduledEvent } from "@/types/event";

export async function GET() {
  const events = await readAllEvents();
  return Response.json({ events });
}

export async function POST(req: NextRequest) {
  try {
    const body = (await req.json()) as Partial<ScheduledEvent> & { deleteId?: string };
    if (body.deleteId) {
      const ok = await deleteEvent(body.deleteId);
      return Response.json({ ok });
    }
    if (!body.id || !body.title || !body.patientName || !body.startIso || !body.recordingKind) {
      return new Response("Missing required fields", { status: 400 });
    }
    const saved = await upsertEvent(body as ScheduledEvent);
    return Response.json({ event: saved });
  } catch (err) {
    console.error(err);
    return new Response("Invalid JSON", { status: 400 });
  }
}
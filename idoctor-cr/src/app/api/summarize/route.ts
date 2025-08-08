import { NextRequest } from "next/server";
import { getOpenAI } from "@/lib/openai";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SYSTEM_PROMPT = `Tu es un(e) secrétaire médical(e). À partir d'une transcription de consultation, produis un compte rendu (CR) structuré, concis et fidèle.
Inclure: Motif, Antécédents pertinents, Examen, Diagnostic/Impression, Conduite à tenir/Prescription, Suivi. Utiliser un style télégraphique, phrases courtes, puces si pertinent. Français.`;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { transcript, patientName, title } = body as { transcript: string; patientName?: string; title?: string };
    if (!transcript) return new Response("transcript required", { status: 400 });

    const client = getOpenAI();
    if (!client) {
      return Response.json({ summary: "[Résumé indisponible en local]" });
    }

    const userContent = `Titre: ${title ?? "Consultation"}\nPatient: ${patientName ?? "N/A"}\n\nTranscription:\n${transcript}`;

    const response = await client.chat.completions.create({
      model: "gpt-4o-mini",
      temperature: 0.2,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: userContent },
      ],
    });

    const summary = response.choices?.[0]?.message?.content ?? "";
    return Response.json({ summary });
  } catch (err) {
    console.error(err);
    return new Response("Invalid request", { status: 400 });
  }
}
import { NextRequest } from "next/server";
import { getOpenAI } from "@/lib/openai";
import { createReadStream } from "fs";
import path from "path";
import { toFile } from "openai/uploads";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { fileUrl, language } = body as { fileUrl: string; language?: string };
    if (!fileUrl) return new Response("fileUrl required", { status: 400 });

    const client = getOpenAI();
    if (!client) {
      return Response.json({ transcript: "[Transcription indisponible en local]" });
    }

    const publicPrefix = "/uploads/";
    if (!fileUrl.startsWith(publicPrefix)) {
      return new Response("Only local /uploads files are supported", { status: 400 });
    }
    const absolutePath = path.join(process.cwd(), "public", fileUrl.replace(publicPrefix, "uploads/"));

    const file = await toFile(createReadStream(absolutePath), path.basename(absolutePath));

    const response = await client.audio.transcriptions.create({
      file,
      model: "gpt-4o-transcribe",
      language,
      response_format: "json",
      temperature: 0.2,
    });

    const text = (response as unknown as { text?: string }).text ?? "";
    return Response.json({ transcript: text });
  } catch (err) {
    console.error(err);
    return new Response("Invalid request", { status: 400 });
  }
}
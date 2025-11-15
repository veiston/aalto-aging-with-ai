"""Gemini STT/LLM/TTS pipeline (Twilio-independent)."""
import os
from typing import Dict, Optional

import numpy as np
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from google.cloud import texttospeech
except ImportError:
    texttospeech = None

from .google_speech_to_text import transcribe_mulaw_audio


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_SYSTEM_PROMPT = os.getenv(
    "GEMINI_SYSTEM_PROMPT",
    "You are a calm aide supporting older adults via phone. Answer clearly, briefly, and safely.",
)
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE_CODE", "en-US")
DEFAULT_SPEAKING_RATE = float(os.getenv("DEFAULT_SPEAKING_RATE", "1.0"))
OUTPUT_SAMPLE_RATE = 8000

if genai and GOOGLE_API_KEY:
    try:
        configure_fn = getattr(genai, "configure", None)
        if configure_fn:
            configure_fn(api_key=GOOGLE_API_KEY)
        model_cls = getattr(genai, "GenerativeModel", None)
        GEMINI_MODEL = model_cls(GEMINI_MODEL_NAME) if model_cls else None
    except Exception:
        GEMINI_MODEL = None
else:
    GEMINI_MODEL = None

if texttospeech:
    try:
        TTS_CLIENT = texttospeech.TextToSpeechClient()
    except Exception:
        TTS_CLIENT = None
else:
    TTS_CLIENT = None


def _context_to_prompt(context: Optional[Dict]) -> str:
    if not context:
        return ""
    parts = [f"{key}: {value}" for key, value in context.items()]
    return " | ".join(parts)


def _extract_text(result) -> str:
    if not result:
        return ""
    if getattr(result, "text", None):
        return result.text.strip()
    candidates = getattr(result, "candidates", [])
    for candidate in candidates:
        if not candidate.content:
            continue
        texts = [getattr(part, "text", "") for part in candidate.content.parts]
        cleaned = " ".join(filter(None, texts)).strip()
        if cleaned:
            return cleaned
    return ""


def generate_gemini_response(user_text: str, context: Optional[Dict] = None) -> str:
    user_text = (user_text or "").strip()
    if not user_text:
        return "I did not hear anything. Could you repeat that?"

    if not GEMINI_MODEL:
        return f"You said: '{user_text}'. This is a fallback response."

    prompt = f"{GEMINI_SYSTEM_PROMPT}\nContext: {_context_to_prompt(context)}\nUser: {user_text}"
    try:
        result = GEMINI_MODEL.generate_content(prompt)
        text = _extract_text(result)
        return text or "I want to be sure I understood. Could you restate that?"
    except Exception:
        return "I'm having trouble reaching the assistant right now."


def synthesize_reply_audio(
    text: str,
    language_code: str = DEFAULT_LANGUAGE,
    speaking_rate: float = DEFAULT_SPEAKING_RATE,
) -> Optional[np.ndarray]:
    if not text or not TTS_CLIENT or not texttospeech:
        return None

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        sample_rate_hertz=8000,
    )

    try:
        response = TTS_CLIENT.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        return np.frombuffer(response.audio_content, dtype=np.int16)
    except Exception:
        return None


def process_voice_turn(
    mulaw_audio_chunk: bytes,
    context: Optional[Dict] = None,
    language_code: str = DEFAULT_LANGUAGE,
    speaking_rate: float = DEFAULT_SPEAKING_RATE,
) -> Dict[str, object]:
    transcript = transcribe_mulaw_audio(mulaw_audio_chunk)
    ai_text = generate_gemini_response(transcript, context)
    linear_audio = synthesize_reply_audio(
        ai_text,
        language_code=language_code,
        speaking_rate=speaking_rate,
    )

    return {
        "transcript": transcript,
        "ai_text": ai_text,
        "linear_audio": linear_audio,
        "sample_rate": OUTPUT_SAMPLE_RATE,
    }


if __name__ == "__main__":
    sample_rate = 8000
    duration = 1
    t = np.arange(sample_rate * duration, dtype=np.float32)
    tone = (np.sin(2 * np.pi * 220 * t / sample_rate) * 1000.0).astype(np.int16)
    from .mulaw_converter import linear_to_mulaw

    mulaw_sample = linear_to_mulaw(tone)

    result = process_voice_turn(
        mulaw_sample,
        context={"scenario": "demo"},
    )
    print({key: (len(val) if isinstance(val, (bytes, bytearray)) else val) for key, val in result.items()})

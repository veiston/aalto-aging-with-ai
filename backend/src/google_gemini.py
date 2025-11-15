"""Gemini STT/LLM/TTS pipeline (Twilio-independent)."""
import os
from typing import Dict, Optional

import numpy as np
from dotenv import load_dotenv
import logging

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

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Preferred model name (will try to use, then fall back dynamically)
PREFERRED_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-preview")
GEMINI_SYSTEM_PROMPT = os.getenv(
    "GEMINI_SYSTEM_PROMPT",
    "You are a calm aide supporting older adults via phone. Answer clearly, briefly, and safely.",
)
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE_CODE", "en-US")
DEFAULT_SPEAKING_RATE = float(os.getenv("DEFAULT_SPEAKING_RATE", "1.0"))
OUTPUT_SAMPLE_RATE = 8000

def _normalize_model_name(name: Optional[str]) -> str:
    if not name:
        return ""
    return name.split("/")[-1]


def _resolve_gemini_model() -> Optional[object]:
    if not genai or not GOOGLE_API_KEY:
        return None
    try:
        configure_fn = getattr(genai, "configure", None)
        if configure_fn:
            configure_fn(api_key=GOOGLE_API_KEY)

        preferred = _normalize_model_name(PREFERRED_GEMINI_MODEL)
        list_models_fn = getattr(genai, "list_models", None)
        model_cls = getattr(genai, "GenerativeModel", None)
        if not model_cls:
            logger.error("google.generativeai.GenerativeModel not available")
            return None

        # If we can list models, pick the best supported; otherwise try preferred then safe fallbacks
        candidate_names: list[str] = []
        if list_models_fn:
            try:
                available = list(list_models_fn())
                supported = [m for m in available if 'generateContent' in getattr(m, 'supported_generation_methods', [])]
                # Normalize names and build ranking
                normalized_supported = [(_normalize_model_name(getattr(m, 'name', '')), m) for m in supported]

                # Rank: exact preferred match -> contains '2.5'+'flash' -> contains '2.0'+'flash' -> contains '1.5'+'flash' -> contains 'pro' -> first
                def score(name: str) -> tuple:
                    return (
                        0 if name == preferred else 1,
                        0 if ('2.5' in name and 'flash' in name) else 1,
                        0 if ('2.0' in name and 'flash' in name) else 1,
                        0 if ('1.5' in name and 'flash' in name) else 1,
                        0 if ('pro' in name) else 1,
                    )

                normalized_supported.sort(key=lambda nm: score(nm[0]))
                candidate_names = [nm for nm, _m in normalized_supported]
            except Exception:
                logger.exception("Failed to list Gemini models; will try direct preferences")

        # If no candidates from listing, try preferred then a set of safe fallbacks
        if not candidate_names:
            candidate_names = [
                preferred,
                "gemini-2.0-flash",
                "gemini-2.0-flash-lite",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]

        # Try to instantiate in order
        for name in candidate_names:
            if not name:
                continue
            try:
                model = model_cls(name)
                # Quick smoke call? Avoid API call; assume construct succeeds
                logger.info(f"Using Gemini model: {name}")
                return model
            except Exception:
                logger.warning(f"Failed to initialize Gemini model '{name}', trying next...", exc_info=True)
                continue

        logger.error("No suitable Gemini model could be initialized.")
        return None
    except Exception:
        logger.exception("Error resolving Gemini model")
        return None


GEMINI_MODEL = _resolve_gemini_model()

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
    except Exception as e:
        logger.exception("Gemini generate_content failed")
        return "I'm having trouble reaching the assistant right now."


def synthesize_reply_audio(
    text: str,
    language_code: str = DEFAULT_LANGUAGE,
    speaking_rate: float = DEFAULT_SPEAKING_RATE,
) -> Optional[np.ndarray]:
    if not text:
        logger.warning("synthesize_reply_audio called with no text.")
        return None
    if not TTS_CLIENT or not texttospeech:
        logger.error("TextToSpeech client not available.")
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
        logger.info(f"Synthesizing audio for text: '{text[:50]}...'")
        response = TTS_CLIENT.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        logger.info("Successfully synthesized audio.")
        return np.frombuffer(response.audio_content, dtype=np.int16)
    except Exception:
        logger.exception("Google Text-to-Speech synthesis failed.")
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

# test function
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

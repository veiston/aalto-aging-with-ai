"""Main Orchestrator for voice pipeline."""
from __future__ import annotations

import base64
import os
from typing import Dict, Optional

import numpy as np
from twilio.twiml.voice_response import VoiceResponse

from .google_gemini import process_voice_turn
from .mulaw_converter import linear_to_mulaw
from .silero_vad import detect_voice_activity
from .twilio_calls import receive_call, setup_twilio_client


def _mulaw_to_numpy(audio_chunk: bytes) -> np.ndarray:
    from .mulaw_converter import mulaw_to_linear

    return mulaw_to_linear(audio_chunk)


def process_audio_chunk(audio_chunk: bytes, context: Dict) -> Optional[Dict[str, object]]:
    linear_audio = _mulaw_to_numpy(audio_chunk)
    if not detect_voice_activity(linear_audio)["has_speech"]:
        return None

    result = process_voice_turn(audio_chunk, context=context)
    if not result:
        return None

    linear_audio_raw = result.get("linear_audio")
    if linear_audio_raw is None:
        return result
    linear_audio_np = (
        linear_audio_raw.astype(np.int16)
        if isinstance(linear_audio_raw, np.ndarray)
        else np.array([], dtype=np.int16)
    )
    mulaw_audio = linear_to_mulaw(linear_audio_np)
    result.update({"linear_audio": linear_audio_np, "mulaw_audio": mulaw_audio})
    return result


def create_twiml_response(mulaw_audio: bytes) -> str:
    if not mulaw_audio:
        response = VoiceResponse()
        response.say("I did not hear anything. Please try again.")
        return str(response)

    encoded_audio = base64.b64encode(mulaw_audio).decode("utf-8")
    response = VoiceResponse()
    response.play(f"data:audio/x-mulaw;base64,{encoded_audio}")
    return str(response)


if __name__ == "__main__":
    print("--- Running Main Orchestrator Test ---")

    client = setup_twilio_client()
    demo_call_sid = os.getenv("TWILIO_DEMO_CALL_SID")
    call_info: Dict[str, str] = {"from": "unknown"}
    if client and demo_call_sid:
        fetched = receive_call(client, demo_call_sid)
        call_info = fetched if isinstance(fetched, dict) else call_info
    elif client:
        print("Skipping Twilio call fetch; no TWILIO_DEMO_CALL_SID set.")
    print(f"Received call from: {call_info.get('from', 'unknown')}")

    user_context = {
        "name": "John Doe",
        "preferences": ["swimming", "reading"],
        "location": "Helsinki",
    }

    sample_rate = 8000
    duration = 2
    silence_data = np.zeros(sample_rate * duration, dtype=np.int16)
    mulaw_silence_chunk = linear_to_mulaw(silence_data)

    print("\n--- Testing with silent audio ---")
    result = process_audio_chunk(mulaw_silence_chunk, user_context)

    mulaw_payload = result.get("mulaw_audio") if result else None
    if isinstance(mulaw_payload, (bytes, bytearray)) and mulaw_payload:
        twiml = create_twiml_response(bytes(mulaw_payload))
        print("TwiML to send back to Twilio:")
        print(twiml)
    else:
        print("No response audio generated, as expected for silent input.")

    print("\n--- Main Orchestrator Test Finished ---")

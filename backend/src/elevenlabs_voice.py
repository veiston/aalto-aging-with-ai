"""
ElevenLabs - Premium Text to Speech
Natural voice for elderly person (Finnish & English)
"""
import os
from dotenv import load_dotenv
load_dotenv()

# from elevenlabs import Client, VoiceSettings
# from elevenlabs.client import ElevenLabsClient

def synthesize_speech(text: str, language: str = "en", voice_id: str = "default") -> bytes:
    """
    Convert text to speech using ElevenLabs
    language: "en" or "fi"
    voice_id: ElevenLabs voice ID
    """
    # client = ElevenLabsClient(api_key=os.environ.get("ELEVENLABS_API_KEY"))
    # audio = client.text_to_speech.convert(
    #     voice_id=voice_id,
    #     text=text,
    #     model_id="eleven_monolingual_v1",
    #     voice_settings=VoiceSettings(
    #         stability=0.5,
    #         similarity_boost=0.75,
    #         use_speaker_boost=True
    #     )
    # )
    # return b"".join(audio)
    
    # Placeholder
    return b"audio_stream_here"

def get_voice_for_language(language: str) -> str:
    """Map language to optimal ElevenLabs voice"""
    voices = {
        "en": "arnold",      # Clear, natural English
        "fi": "Aino-FI"      # Finnish speaker
    }
    return voices.get(language, "arnold")

def create_elderly_greeting(name: str, language: str = "en") -> bytes:
    """Generate personalized greeting"""
    greetings = {
        "en": f"Hello {name}, how can I help you today?",
        "fi": f"Terve {name}, miten voin auttaa sinua tänään?"
    }
    
    text = greetings.get(language, greetings["en"])
    voice = get_voice_for_language(language)
    return synthesize_speech(text, language, voice)

def create_reminder_message(message: str, language: str = "en") -> bytes:
    """Generate reminder with natural pacing"""
    # Add pauses for clarity
    if language == "fi":
        formatted = f"{message}. Kiitos."
    else:
        formatted = f"{message}. Thank you."
    
    voice = get_voice_for_language(language)
    return synthesize_speech(formatted, language, voice)

if __name__ == "__main__":
    # Test: English greeting
    audio_en = create_elderly_greeting("Liisa", language="en")
    print(f"English greeting: {len(audio_en)} bytes")
    
    # Test: Finnish greeting
    audio_fi = create_elderly_greeting("Liisa", language="fi")
    print(f"Finnish greeting: {len(audio_fi)} bytes")
    
    # Test: Finnish reminder
    reminder_fi = create_reminder_message("Lääkkeen aika", language="fi")
    print(f"Finnish reminder: {len(reminder_fi)} bytes")
    
    # Test: English reminder
    reminder_en = create_reminder_message("Time for medication", language="en")
    print(f"English reminder: {len(reminder_en)} bytes")

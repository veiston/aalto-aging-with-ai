"""
Google Gemini - Alternative AI Choice
Same as OpenAI but using Google's API for flexibility
"""
import os
from dotenv import load_dotenv
load_dotenv()
import numpy as np
try:
    import google.generativeai as genai
except Exception:
    genai = None

# Local imports for audio processing
from google_speech_to_text import transcribe_mulaw_audio
import mulaw_converter


def generate_gemini_response(user_text: str, context: dict) -> str:
    """
    Get AI response using Google Gemini
    Alternative to OpenAI
    """
    # If google generative library is available, configure with env API key
    if genai and os.environ.get("GOOGLE_API_KEY"):
        try:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            model = genai.get_model("chat-bison") if hasattr(genai, "get_model") else None
            if model:
                resp = model.generate("Help elderly: {}\nUser: {}".format(context, user_text))
                return getattr(resp, "text", str(resp))
        except Exception:
            pass

    # Placeholder fallback
    return f"You said: '{user_text}'. There's a swimming lesson at 3 PM"

def generate_gemini_response_from_audio(mulaw_audio_chunk: bytes, context: dict) -> str:
    """
    Transcribes audio and gets an AI response using Google Gemini.

    Args:
        mulaw_audio_chunk: A bytes object containing the mu-law encoded audio data.
        context: A dictionary containing context for the AI model.

    Returns:
        The AI's response as a string.
    """
    # First, transcribe the audio chunk to text
    transcribed_text = transcribe_mulaw_audio(mulaw_audio_chunk)
    
    if not transcribed_text:
        return "I'm sorry, I didn't catch that. Could you please say it again?"

    # Then, get the AI response based on the transcribed text
    return generate_gemini_response(transcribed_text, context)


def gemini_text_to_speech(text: str) -> bytes:
    """
    Convert text to speech using Google
    (May use Google Cloud Text-to-Speech separately)
    """
    # from google.cloud import texttospeech
    # client = texttospeech.TextToSpeechClient()
    # synthesis_input = texttospeech.SynthesisInput(text=text)
    # voice = texttospeech.VoiceSelectionParams(language_code="en-US")
    # response = client.synthesize_speech(...)
    # return response.audio_content
    
    # Placeholder
    return b"google_audio_here"

if __name__ == "__main__":
    # --- Test 1: Text-based Gemini response ---
    print("--- Running Text-based Test ---")
    text_response = generate_gemini_response(
        "How do I make soup",
        context={"dietary": "low-sodium", "allergies": []}
    )
    print("Gemini Response:", text_response)
    
    audio = gemini_text_to_speech(text_response)
    print("Google TTS audio:", len(audio), "bytes")
    print("-" * 20)

    # --- Test 2: Audio-based Gemini response ---
    # This test requires a configured Google Cloud project for transcription.
    print("\n--- Running Audio-based Test ---")
    # a. Create a dummy mu-law audio chunk (as if from Twilio)
    # This is a silent audio chunk for testing the pipeline without real speech.
    # The transcription will be empty, and the model should handle it gracefully.
    sample_rate = 8000
    duration = 1  # 1 second of silence
    silence_data = np.zeros(sample_rate * duration, dtype=np.int16)
    mulaw_silence = mulaw_converter.linear_to_mulaw(silence_data)

    # b. Process the silent audio chunk
    # Expected: The system will say it didn't understand.
    audio_response = generate_gemini_response_from_audio(
        mulaw_silence,
        context={"user_id": "12345"}
    )
    print("Response from silent audio:", audio_response)

    # To test with actual speech, you would need to load a real audio file.
    # For example:
    # with open("path/to/your/audio.mulaw", "rb") as f:
    #     real_mulaw_audio = f.read()
    # real_response = generate_gemini_response_from_audio(real_mulaw_audio, context={})
    # print("Response from real audio:", real_response)
    print("--- Audio Test Finished ---")

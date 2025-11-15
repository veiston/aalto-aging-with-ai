"""
Main Backend Orchestrator

This script will be the main entry point for the backend application.
It will handle incoming requests (e.g., from Twilio), process the audio,
and generate responses using the various AI services.
"""
# Import necessary modules from the project
from elevenlabs_voice import generate_elevenlabs_speech
from google_gemini import generate_gemini_response, gemini_text_to_speech
from google_speech_to_text import transcribe_linear_audio
from mulaw_converter import mulaw_to_linear, linear_to_mulaw
from openai_voice import generate_openai_speech
from silero_vad import is_speech
from twilio_calls import receive_call, make_reminder_call
from web_search import get_nearby_activities
from whisper_stt import transcribe_audio_whisper

# --- Web Server Setup (Placeholder) ---
# In a real application, this would be a web server like Flask or FastAPI
# that listens for webhooks from Twilio.
#
# Example with Flask:
# from flask import Flask, request
#
# app = Flask(__name__)
#
# @app.route("/handle-call", methods=["POST"])
def handle_call():
    # The audio data would be in the request from Twilio
    # audio_chunk = request.get_data() 
    # response_audio = process_audio_chunk(audio_chunk)
    # # We would then need to return a TwiML response with the audio
    # return create_twiml_response(response_audio)
    pass

def process_audio_chunk(audio_chunk: bytes, context: dict) -> bytes:
    """
    This is the core logic for processing a single chunk of audio.
    It converts audio, detects speech, transcribes, gets an AI response,
    and synthesizes the response back to audio.
    """
    print("Processing audio chunk...")

    # 1. Convert mu-law audio from Twilio to linear PCM for processing.
    # This is done once at the beginning for efficiency.
    linear_audio = mulaw_to_linear(audio_chunk)

    # 2. Use Silero VAD to check if there is speech in the audio.
    # Note: is_speech might need to be adapted to work with chunks.
    if not is_speech(linear_audio):
        print("No speech detected in chunk.")
        return None # Return nothing if no speech is detected

    print("Speech detected, proceeding with transcription and AI response.")

    # 3. Transcribe the audio to text using the linear audio data.
    transcribed_text = transcribe_linear_audio(linear_audio)
    if not transcribed_text:
        print("Transcription resulted in empty text.")
        # We can decide if we want to say something like "I didn't hear you clearly"
        return None 
    
    print(f"Transcribed text: '{transcribed_text}'")

    # 4. Generate a response using Google Gemini with the transcribed text.
    ai_response_text = generate_gemini_response(transcribed_text, context)
    print(f"AI Response: {ai_response_text}")

    # 5. Convert the AI's text response back to speech.
    # We have multiple options, let's use ElevenLabs for this example.
    response_audio_linear = generate_elevenlabs_speech(ai_response_text)
    print(f"Generated {len(response_audio_linear)} bytes of speech.")

    # 6. Convert the linear response audio back to mu-law for Twilio.
    response_mulaw = linear_to_mulaw(response_audio_linear)

    return response_mulaw

def create_twiml_response(audio_chunk_mulaw: bytes):
    """
    Creates a TwiML response to play audio back to the user.
    (This is a placeholder for the actual Twilio library usage).
    """
    # In a real Flask app, you'd return XML like this:
    # from twilio.twiml.voice_response import VoiceResponse, Play
    # import base64
    #
    # response = VoiceResponse()
    # encoded_audio = base64.b64encode(audio_chunk_mulaw).decode('utf-8')
    # response.play(f"data:audio/x-mulaw;base64,{encoded_audio}")
    # return str(response)
    print("Creating TwiML response (placeholder).")
    return f"<Response><Play>...</Play></Response>"


if __name__ == "__main__":
    # This is a test block to simulate the process.
    # In a real scenario, the web server would be running.
    print("--- Running Main Orchestrator Test ---")

    # 1. Simulate receiving a call and getting context
    call_info = receive_call(None, "CALL_SID_DUMMY")
    print(f"Received call from: {call_info['from']}")
    
    # This would be retrieved from a database based on the caller's number
    user_context = {
        "name": "John Doe",
        "preferences": ["swimming", "reading"],
        "location": "Helsinki"
    }

    # 2. Simulate receiving an audio chunk (e.g., from a file)
    # For this test, we'll create a dummy silent audio chunk.
    # In a real test, you'd load a file with actual speech.
    import numpy as np
    sample_rate = 8000
    duration = 2  # seconds
    silence_data = np.zeros(sample_rate * duration, dtype=np.int16)
    mulaw_silence_chunk = linear_to_mulaw(silence_data)

    # 3. Process the audio chunk
    # With silent audio, this should be caught by the VAD and return None.
    print("\n--- Testing with silent audio ---")
    response_audio = process_audio_chunk(mulaw_silence_chunk, user_context)

    # 4. Create and "send" the TwiML response
    if response_audio:
        twiml = create_twiml_response(response_audio)
        print("TwiML to send back to Twilio:")
        print(twiml)
    else:
        print("No response audio generated, as expected for silent input.")

    print("\n--- Main Orchestrator Test Finished ---")

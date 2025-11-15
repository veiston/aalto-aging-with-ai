"""
Google Cloud Speech-to-Text
This script transcribes audio chunks, specifically handling mu-law encoded audio
from services like Twilio, and sends it to Google's Speech-to-Text API.
"""
import os
from dotenv import load_dotenv
load_dotenv()
import numpy as np
from google.cloud import speech
import mulaw_converter

# --- Authentication Note ---
# This script uses Google Cloud's Application Default Credentials (ADC).
# Before running, ensure you have authenticated with Google Cloud CLI or
# have set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# For example:
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    if os.environ.get("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY found in environment. Note: Speech-to-Text typically requires service account credentials for full features.")
    else:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Authentication may fail. Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_API_KEY in your .env file.")

def transcribe_linear_audio(linear_audio_np: np.ndarray, sample_rate: int = 8000, language_code: str = "en-US") -> str:
    """
    Transcribes a linear PCM audio chunk using Google Cloud Speech-to-Text.

    Args:
        linear_audio_np: A NumPy array containing the linear PCM audio data.
        sample_rate: The sample rate of the audio.
        language_code: The language code for transcription.

    Returns:
        The transcribed text as a string.
    """
    # 1. Get the raw bytes from the numpy array for the API
    linear_audio_bytes = linear_audio_np.tobytes()

    # 2. Instantiate the Speech-to-Text client
    try:
        client = speech.SpeechClient()
    except Exception as e:
        print(f"Error creating SpeechClient: {e}")
        print("Please ensure you have authenticated correctly.")
        return ""

    # 3. Configure the recognition request
    recognition_audio = speech.RecognitionAudio(content=linear_audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
    )

    # 4. Send the request and get the response
    try:
        response = client.recognize(config=config, audio=recognition_audio)
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""

    # 5. Process the response and extract the transcript
    transcripts = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcripts)


def transcribe_mulaw_audio(mulaw_audio_chunk: bytes, sample_rate: int = 8000) -> str:
    """
    Transcribes a mu-law encoded audio chunk by converting it to linear PCM first.

    Args:
        mulaw_audio_chunk: A bytes object containing the mu-law encoded audio data.
        sample_rate: The sample rate of the audio.

    Returns:
        The transcribed text as a string.
    """
    # Convert mu-law audio to linear PCM
    linear_audio_np = mulaw_converter.mulaw_to_linear(mulaw_audio_chunk)
    
    # Transcribe the linear audio
    return transcribe_linear_audio(linear_audio_np, sample_rate)


if __name__ == "__main__":
    # This is a test block. To run it, you need:
    # 1. `pip install google-cloud-speech numpy`
    # 2. A configured Google Cloud project with the Speech-to-Text API enabled.
    # 3. Authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS).

    print("Running a test transcription...")

    # a. Create a dummy audio signal (a simple sine wave)
    sample_rate = 8000
    duration = 2  # seconds
    frequency = 440  # Hz (A4 note)
    t = np.linspace(0., duration, int(sample_rate * duration), endpoint=False)
    amplitude = np.iinfo(np.int16).max * 0.5
    data = amplitude * np.sin(2. * np.pi * frequency * t)
    linear_pcm_data = data.astype(np.int16)

    # b. Test the linear transcription function directly
    print("\nTesting transcription with linear PCM data...")
    transcript_linear = transcribe_linear_audio(linear_pcm_data, sample_rate)
    if transcript_linear:
        print(f"Transcription result from linear: '{transcript_linear}'")
    else:
        print("Transcription from linear returned no result, as expected for a non-speech audio test.")

    # c. Convert it to mu-law to test the wrapper function
    print("\nTesting transcription with mu-law data...")
    mulaw_data = mulaw_converter.linear_to_mulaw(linear_pcm_data)
    transcript_mulaw = transcribe_mulaw_audio(mulaw_data, sample_rate)

    if transcript_mulaw:
        print(f"Transcription result from mulaw: '{transcript_mulaw}'")
    else:
        print("Transcription from mulaw returned no result, as expected for a non-speech audio test.")
    
    print("\nTest finished.")

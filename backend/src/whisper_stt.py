"""
Whisper - Speech to Text
Converts elderly person's voice to text
"""
import numpy as np
# from openai import OpenAI

def transcribe_audio(audio_data: np.ndarray, language: str = "en") -> dict:
    """
    Convert speech to text
    """
    # client = OpenAI()
    # result = client.audio.transcriptions.create(
    #     model="whisper-1",
    #     file=audio_file,
    #     language=language
    # )
    # return {"text": result.text}
    
    # Placeholder: simulate transcription
    return {
        "text": "What should I do today",
        "language": language,
        "confidence": 0.95
    }

if __name__ == "__main__":
    # Test: transcribe sample
    audio = np.random.randn(16000).astype(np.float32)
    result = transcribe_audio(audio, language="en")
    print("Transcribed:", result)

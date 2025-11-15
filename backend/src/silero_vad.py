"""
Silero VAD - Voice Activity Detection
Detects when elderly person is speaking vs silence
"""
import numpy as np
# from silero_vad import load_silero_vad

def detect_voice_activity(audio_chunk: np.ndarray, sample_rate: int = 16000) -> dict:
    """
    Detect if audio contains speech
    """
    # model = load_silero_vad()
    # speech_prob = model(audio_chunk, sample_rate)
    
    # Simple placeholder: detect volume threshold
    rms = np.sqrt(np.mean(audio_chunk**2))
    has_speech = rms > 0.02
    
    return {
        "has_speech": has_speech,
        "confidence": float(rms)
    }



if __name__ == "__main__":
    # Test: silent audio
    silent = np.zeros(16000, dtype=np.float32)
    print("Silent audio:", detect_voice_activity(silent))
    
    # Test: noise audio
    noise = np.random.normal(0, 0.1, 16000).astype(np.float32)
    print("Noise audio:", detect_voice_activity(noise))

"""
Mu-law Codec - Audio Compression
Compresses audio for phone transmission (Twilio standard)
"""
import numpy as np

def linear_to_mulaw(linear_audio: np.ndarray, max_value: int = 32768) -> bytes:
    """Convert linear PCM to mu-law compressed audio"""
    mu = 255.0
    # Normalize to [-1, 1]
    normalized = linear_audio.astype(np.float32) / max_value
    normalized = np.clip(normalized, -1, 1)
    
    # Mu-law encoding
    abs_val = np.abs(normalized)
    magnitude = np.log(1 + mu * abs_val) / np.log(1 + mu)
    signal = np.sign(normalized) * magnitude
    quantized = np.uint8((signal + 1) * 127.5)
    return quantized.tobytes()

def mulaw_to_linear(mulaw_audio: bytes, max_value: int = 32768) -> np.ndarray:
    """Convert mu-law back to linear PCM"""
    quantized = np.frombuffer(mulaw_audio, dtype=np.uint8).astype(np.float32)
    signal = (quantized / 127.5) - 1.0
    
    mu = 255.0
    magnitude = np.abs(signal)
    linear = np.sign(signal) * (1.0 / mu) * (np.power(1.0 + mu, magnitude) - 1.0)
    return (linear * max_value).astype(np.int16)

if __name__ == "__main__":
    # Test: encode and decode
    original = np.array([100, 500, -200, 0], dtype=np.int16)
    print("Original:", original)
    
    compressed = linear_to_mulaw(original.astype(np.float32))
    print("Compressed size:", len(compressed), "bytes")
    
    recovered = mulaw_to_linear(compressed)
    print("Recovered:", recovered[:4])

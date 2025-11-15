"""
OpenAI Voice - Text to Speech + AI Responses
Creates natural voice responses for elderly users
"""
import os
from dotenv import load_dotenv
load_dotenv()

# from openai import OpenAI

def generate_voice_response(text: str, voice: str = "alloy") -> bytes:
    """
    Convert text to speech using OpenAI
    voice: alloy, echo, fable, onyx, nova, shimmer
    """
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # response = client.audio.speech.create(
    #     model="tts-1",
    #     voice=voice,
    #     input=text
    # )
    # return response.content
    
    # Placeholder
    return b"audio_data_here"

def get_ai_response(user_text: str, context: dict) -> str:
    """
    Get AI response using OpenAI
    context: elderly person's profile info
    """
    # client = OpenAI()
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": f"Help elderly person: {context}"},
    #         {"role": "user", "content": user_text}
    #     ]
    # )
    # return response.choices[0].message.content
    
    # Placeholder
    return "There's a yoga class at 2 PM nearby"

if __name__ == "__main__":
    # Test: generate response and voice
    response_text = get_ai_response(
        "What should I do today",
        context={"age": 75, "interests": ["yoga", "gardening"]}
    )
    print("AI Response:", response_text)
    
    audio = generate_voice_response(response_text, voice="nova")
    print("Audio generated:", len(audio), "bytes")

import base64
import json
import logging
from fastapi import FastAPI, Request, WebSocket, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Connect

from sqlmodel import SQLModel
from .database import engine
from .routers import surveys, responses
from .main import process_audio_chunk
from .google_gemini import process_voice_turn
from .mulaw_converter import linear_to_mulaw

import wave
import io
import requests 
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
SQLModel.metadata.create_all(engine)

app.include_router(surveys.router)
app.include_router(responses.router)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/voice_record")
async def voice_record():
    """Simplest Twilio flow: record a short utterance, then process it."""
    resp = VoiceResponse()
    resp.say("Hello. After the beep, please say something to our AI.")
    resp.record(action="/process_recording", method="POST", play_beep=True, max_length=8, trim="do-not-trim")
    return PlainTextResponse(str(resp), media_type="text/xml")

@app.post("/process_recording")
async def process_recording(RecordingUrl: str = Form(...)):
    """Download the recording, run Gemini, reply with Twilio TTS via <Say>."""
    # Twilio provides a URL without extension. Append .wav to get the audio file.
    wav_url = RecordingUrl + ".wav"
    try:
        r = requests.get(wav_url, timeout=15)
        if r.status_code == 401 or r.status_code == 403:
            # Try again with Twilio auth if private
            from os import environ
            sid = environ.get("TWILIO_ACCOUNT_SID")
            token = environ.get("TWILIO_AUTH_TOKEN")
            if sid and token:
                r = requests.get(wav_url, auth=(sid, token), timeout=15)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to download recording from {wav_url}: {e}")
        vr = VoiceResponse()
        vr.say("Sorry, I couldn't retrieve your recording. Please try again later.")
        return PlainTextResponse(str(vr), media_type="text/xml")

    try:
        with wave.open(io.BytesIO(r.content), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)
    except wave.Error as e:
        logger.error(f"Error reading WAV content: {e}")
        vr = VoiceResponse()
        vr.say("Sorry, the audio format was not supported. Please try again.")
        return PlainTextResponse(str(vr), media_type="text/xml")

    # Expect 16-bit PCM mono. If stereo, take first channel.
    dtype = np.int16 if sampwidth == 2 else np.int16
    pcm = np.frombuffer(raw, dtype=dtype)
    if n_channels == 2:
        pcm = pcm[::2]

    # Convert linear PCM to mu-law bytes for our pipeline
    mulaw_bytes = linear_to_mulaw(pcm)

    user_context = {"name": "Caller"}
    result = process_voice_turn(mulaw_bytes, context=user_context) or {}
    ai_text = result.get("ai_text") or result.get("transcript") or "Sorry, I couldn't process that."

    vr = VoiceResponse()
    vr.say(ai_text)
    return PlainTextResponse(str(vr), media_type="text/xml")

@app.post("/voice")
async def voice(request: Request):
    """Handle incoming Twilio voice calls by connecting to a WebSocket stream."""
    host = request.url.hostname
    port = request.url.port
    
    # Construct WebSocket URL, handling standard and non-standard ports
    ws_url = f"wss://{host}"
    if port and port not in [80, 443]:
        ws_url += f":{port}"
    ws_url += "/ws"

    logger.info(f"Incoming call, connecting to WebSocket at {ws_url}")

    response = VoiceResponse()
    connect = Connect()
    connect.stream(url=ws_url)
    response.append(connect)
    # Keep the call alive while waiting for user to speak
    response.pause(length=30)

    return PlainTextResponse(str(response), media_type='text/xml')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle the WebSocket audio stream from Twilio."""
    await websocket.accept()
    logger.info("WebSocket connection accepted.")
    
    # This context would eventually be loaded from a database based on the caller's number
    user_context = {
        "name": "John Doe",
        "preferences": ["swimming", "reading"],
        "location": "Helsinki",
    }

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            if data['event'] == 'start':
                logger.info(f"Twilio 'start' event received for stream {data['streamSid']}.")
            
            elif data['event'] == 'media':
                audio_chunk = base64.b64decode(data['media']['payload'])
                
                result = process_audio_chunk(audio_chunk, user_context)
                
                if result and result.get("mulaw_audio"):
                    mulaw_payload = result["mulaw_audio"]
                    
                    if isinstance(mulaw_payload, (bytes, bytearray)):
                        # Base64-encode the mu-law audio and prepare it for Twilio
                        encoded_audio = base64.b64encode(mulaw_payload).decode('utf-8')
                        
                        media_message = {
                            "event": "media",
                            "streamSid": data['streamSid'],
                            "media": {
                                "payload": encoded_audio
                            }
                        }
                        
                        # Send the synthesized audio back to Twilio
                        await websocket.send_text(json.dumps(media_message))

            elif data['event'] == 'stop':
                logger.info(f"Twilio 'stop' event received for stream {data['streamSid']}. Closing WebSocket.")
                break

    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        logger.info("WebSocket connection closed.")
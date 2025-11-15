# Quick Setup Guide

## 1. Start the Server

```bash
# From project root
.venv\Scripts\python.exe -m uvicorn backend.src.server:app --reload --host 0.0.0.0 --port 8000
```

Server runs on: `http://localhost:8000`

## 2. Expose with ngrok

**Install ngrok** (if not already installed):

- Download from: https://ngrok.com/download
- Or via Chocolatey: `choco install ngrok`
- Or via Scoop: `scoop install ngrok`

**Run ngrok:**

```bash
ngrok http 8000
```

Copy the `https://` forwarding URL (e.g., `https://abc123.ngrok-free.app`)

## 3. Configure Twilio

1. Go to: https://console.twilio.com/
2. Navigate to: Phone Numbers → Manage → Active Numbers
3. Click your number: `+15075568288`
4. Under "Voice Configuration":
   - **A CALL COMES IN**: Webhook
   - **URL**: `https://YOUR_NGROK_URL/voice_record`
   - **HTTP**: POST
5. Click **Save**

## 4. Test the Flow

Call `+15075568288` and:

1. Hear: "Hello. After the beep, please speak a short question."
2. Speak your question (up to 8 seconds)
3. AI processes with Gemini
4. Hear the AI response

## API Endpoints

- `GET /` - Health check
- `POST /voice_record` - Simple record & respond flow (recommended for MVP)
- `POST /voice` - WebSocket stream setup (for advanced use)
- `WebSocket /ws` - Real-time audio streaming

## Environment Variables

Ensure `.env` has:

```
TWILIO_ACCOUNT_SID=ACb7ec9f665735dedf209df4a70f721ca8
TWILIO_AUTH_TOKEN=477213dde4d6baa062d6615c3fe70e4f
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Homo_ludens\Documents\GitHub\aalto-aging-with-ai\gen-lang-client-0229205555-b3129e6b2e73.json
GOOGLE_API_KEY=AIzaSyCbjQtWL9Agyc0kikLkPCsLtOXLps8PgDo
```

## Troubleshooting

**Server won't start:**

- Install dependencies: `.venv\Scripts\pip.exe install -r backend\requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

**ngrok URL changes:**

- Free ngrok URLs change every restart
- Update Twilio webhook each time
- Or upgrade to ngrok paid for static URLs

**No audio response:**

- Check Google Cloud Speech API is enabled
- Verify service account JSON path
- Check server logs for errors

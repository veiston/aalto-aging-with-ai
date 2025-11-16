# 📞 Easy Call Help

## Twilio

+15075568288

**One line**  
A voice‑based participation platform where older adults shape society through simple phone conversations.

---

## 🎯 Problem

- Many older adults remain unreachable online  
- Digital surveys miss those with the most lived experience  
- Loneliness and low participation reduce well‑being  
- Institutions lack affordable access to older adults’ input 

## 📗 Solution

**Easy Call Help**  
A phone‑based survey system that lets older adults answer institutional questions through natural voice conversations. No apps, no screens, no digital skills required.

---

## ⭐ How It Works

1. A verified institution creates a survey in the dashboard  
2. The backend stores questions in a structured format  
3. The system converts questions into natural dialogue  
4. The voice assistant calls participants  
5. Older adults answer by speaking normally  
6. Responses are converted into clean text  
7. The institution views results in the dashboard  

---

## 👥 Who it helps

Older adults, people living alone, municipalities, researchers.

---

## 🔧 Tech stack

- FastAPI + SQLModel backend server with Twilio webhooks
- Google Gemini (LLM + TTS)
- Google Cloud Speech-to-Text
- Silero VAD for voice activity detection
- Mu-law audio codec for telephony
- Next.js dashboard (frontend)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Twilio account with phone number
- Google Cloud account with Speech-to-Text and Text-to-Speech APIs enabled
- Google Gemini API key
- ngrok (for local testing)

### Setup

1. **Clone and install dependencies:**

```bash
git clone https://github.com/veiston/aalto-aging-with-ai.git
cd aalto-aging-with-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

2. **Configure environment variables:**

- Copy `.env.example` to `.env`
- Fill in your credentials:
  - Twilio: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
  - Google: `GOOGLE_APPLICATION_CREDENTIALS` (path to service account JSON), `GOOGLE_API_KEY`

3. **Start the server:**

```bash
.venv\Scripts\python.exe -m uvicorn backend.src.server:app --host 0.0.0.0 --port 8000
```

4. **Expose with ngrok in new terminal:**

```bash
ngrok http 8000 --region eu
```

Copy the https URL (e.g., `https://abc123.ngrok-free.app`)

5. **Configure Twilio webhook:**

- Go to Twilio Console → Phone Numbers
- Select your number
- Set "A call comes in" webhook to: `https://YOUR_NGROK_URL/voice_record` (POST)
- Save

6. **Test:**
   Call your Twilio number and speak after the beep!

## API Endpoints

### Voice
- `GET /` - Health check
- `POST /voice_record` - Main call handler (record → Gemini → reply)
- `POST /voice` + `WebSocket /ws` - Real-time streaming (advanced)


### Surveys
- `POST /surveys/create` — Create survey  
- `GET /surveys/list` — List all surveys  
- `GET /surveys/details/{id}` — Survey details  
- `DELETE /surveys/delete/{id}` — Delete survey  

### Responses
- `POST /responses/create` — Submit response  
- `GET /responses/list/{survey_id}` — List responses  
- `GET /responses/details/{response_id}` — Response details  
---

## 🛠️ Next steps

Build call flows, implement survey importer, test readiness analysis rules, integrate event data, and run an early pilot.

---

## 📩 Contact

Open an issue to collaborate.

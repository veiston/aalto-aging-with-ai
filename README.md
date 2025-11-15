# 📞 Easy Call Help

## Twilio

+15075568288

**One line**  
A simple voice based AI phone line that supports older adults, families, and researchers, no apps needed.

---

## 🎯 Goal

Increase independence, reduce tech friction, and create a safe communication channel between older adults, families, and research teams.

---

## 📗 What it does

### 🧩 Daily support

- Answers questions with simple speech
- Suggests nearby activities (no booking)
- Gives reminder calls
- Routes the call to the best matched family member when appropriate
- Can search the web to give real time factual information regarding topics the elderly person is looking for.

### 👪 Family profile

Relatives set up an initial profile containing:

- Family relations
- Disabilities, past injuries, medications
- Stress points, communication preferences  
  The system uses this for safer, personalized interactions.

### 🔬 Scientific survey engine (new idea)

Researchers upload text surveys.  
AI converts them into natural phone interviews, runs the full call, records answers, and returns clean datasets.  
This gives universities, cities, and UX teams affordable access to older adults, a group normally very hard and expensive to reach.

### 🎙️ Voice state analysis (new idea)

Before each survey or longer conversation, the AI analyzes the first seconds of speech:  
pause length, speech rate, variability, rhythmic stability, loudness.  
This estimates cognitive readiness and avoids overload by postponing when the person sounds fatigued.

### 🚨 Health and wellbeing signals

Detects early signs of decline or emergencies from pattern changes:  
missed calls, slower speech, confusion spikes, changes in routine.  
Sends alerts to a designated relative.  
Never diagnoses, only notifies about patterns.

### 📊 Opinion and micro statistics

Runs short in call micro surveys.  
Collects anonymized opinions and self reported data for city planning, social care, and research.

---

## ⭐ Feature list

- Voice first phone interactions
- Daily support and reminders
- Family configured context and routing
- Scientific surveys by phone
- Voice based readiness analysis
- Early pattern detection and alerts
- Micro surveys and statistics
- Multilingual simple language

---

## 👥 Who it helps

Older adults, people living alone, families who need early signals, municipalities, researchers, and UX teams.

---

## 🔧 Tech stack

- FastAPI backend server with Twilio webhooks
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
ngrok http 8000
```

Copy the https URL (e.g., `https://abc123.ngrok-free.app`)

5. **Configure Twilio webhook:**

- Go to Twilio Console → Phone Numbers
- Select your number
- Set "A call comes in" webhook to: `https://YOUR_NGROK_URL/voice_record` (POST)
- Save

6. **Test:**
   Call your Twilio number and speak after the beep!

### API Endpoints

- `GET /` - Health check
- `POST /voice_record` - Main call handler (record → Gemini → reply)
- `POST /voice` + `WebSocket /ws` - Real-time streaming (advanced)

## 🤖 What ChatGPT can do now

- Understand voice prompts
- Summarize, explain, translate
- Generate dialog structures
- Do intent and slot extraction

---

## 🚫 What the system cannot do

- Book anything or make external reservations
- Guarantee real time local data
- Manage identity or verify consent alone
- Diagnose medical conditions
- Replace human review for emergency alerts

---

## 🛠️ Next steps

Build call flows, implement survey importer, test readiness analysis rules, integrate event data, and run an early pilot.

---

## 📩 Contact

Open an issue to collaborate.

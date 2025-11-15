## Roadmap — Crucial First (MVP & Hackathon 2025)

Goal: Build the smallest reliable voice-first system that lets older adults call, hear helpful responses, and lets us measure speech & behavior signals for health evaluation.

Priority principles:

- Security & consent first: explicit consent flows, encrypted storage, short retention.
- Minimal external dependencies for the MVP (use mockable interfaces/APIs).
- Fast feedback loop: short pilot (10 users) with daily reminders + weekly check-ins.

Phase 0 — Foundation (One-day sprint)

- Hour 0–1: Set up Twilio webhook skeleton and local server (ngrok if needed).
- Hour 1–2: Implement simple audio intake: accept audio chunks, store to /tmp, return quick ACK.
- Hour 2–3: Wire Silero VAD call to detect speech segments from stored chunks.
- Hour 3–4: Add µ‑law conversion utilities and test roundtrip encode/decode.
- Hour 4–5: Hook Whisper (mock or real) to transcribe a single speech segment; save transcript.
- Hour 5–6: Add placeholder TTS (ElevenLabs mock) and return audio as response.
- Hour 6–7: Implement minimal speech-feature extractor (pause length, words/sec) and output JSON.
- Hour 7–8: End-to-end smoke test: call -> VAD -> STT -> scorer -> TTS reply; prepare demo script.
- Hour 8–9: Polish consent prompt and logging; ensure transcripts and flags stored securely.
- Hour 9–10: Final demo rehearsals, deploy ngrok, record short video or set up live demo.

Minimal success criteria (end of day):

- Receive a call with audio, detect speech, transcribe, generate a reply, and display a JSON score.
- Demo script working for a 2-minute live demo.

Phase 1 — Voice I/O & Pipeline (Day 1–7)

- Real-time VAD (Silero) to detect speech segments.
- µ-law encode/decode for Twilio compatibility (reliable conversion).
- Ingest audio chunks into STT pipeline; persist raw and processed audio separately.

Phase 2 — STT / TTS Integration (Day 2–10)

- Whisper for transcription (local or API) with timestamps.
- Pluggable TTS adapters: ElevenLabs (fi/en), OpenAI voice, Google Gemini TTS — swap easily.
- Short scripts: greetings, reminders, short survey flow.

Phase 3 — Health & Credibility Signals (MVP scoring) (Day 4–14)

- Define core speech features: pause durations, speech rate, word-finding hesitations, pitch variance.
- Build a lightweight scorer that tracks trends per user and emits simple flags (e.g., "attention drop", "slower speech").
- Instrument behavior signals: call frequency, answer delay, repetition count.

Phase 4 — Surveying & Structured Data (Day 7–18)

- Short, consented scientific surveys via voice (3–5 questions).
- Store structured responses and map to health/credibility metrics.
- Simple analytics: weekly deltas per user, pilot cohort aggregation.

Phase 5 — Family Connector & Consent Workflow (Day 10–21)

- One‑button transfer and recorded consent script.
- Consent logs and family contact matching (suggest best contact based on topic / availability).
- Manual escalation UI (operator dashboard) for reviewed flags.

Phase 6 — Pilot, Privacy & Ops (Day 14–28)

- Run 10-person pilot: daily reminder + 1 weekly check-in call.
- Collect metrics: engagement, flag rate, survey completion, false positives.
- Privacy review, encrypted storage, minimal retention policy, and consent audit logging.

Deliverables for Hackathon 2025

- Working demo: call in -> VAD -> Whisper transcript -> AI response (TTS) -> record metrics.
- Dashboard (simple) showing per-user trend graphs (speech rate, pauses) and flags.
- Short pitch doc + 2-minute demo script.

Next steps (immediately actionable)

- Implement Twilio webhook + local worker that runs VAD on incoming segments.
- Hook Whisper for quick STT and wire a placeholder TTS (ElevenLabs mock).
- Define 3 speech features and implement first scorer; add a simple JSON output for dashboarding.

Notes & tradeoffs

- MVP focuses on detection & measurement, not autonomous intervention. Human-in-the-loop for escalation.
- Keep data minimal: store features + short transcript excerpts; avoid full long-term raw audio storage unless needed and consented.

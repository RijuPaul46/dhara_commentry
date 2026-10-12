# Dhaaraa Commentary (ধারা Commentary) 🏏🎙️

A real-time AI cricket commentary prototype that turns ball-by-ball cricket action into spoken commentary in 10 Indian languages with custom commentator personas, powered by **Sarvam AI**.

---

## Features
- **10 Indian Languages Supported**: Bengali (`bn-IN`), Hindi (`hi-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Kannada (`kn-IN`), Malayalam (`ml-IN`), Marathi (`mr-IN`), Gujarati (`gu-IN`), Punjabi (`pa-IN`), and Indian English (`en-IN`).
- **4 Commentator Personas**:
  - *Excited fan* (High energy, passionate celebrations and reactions)
  - *Wise old uncle* (Nostalgic, warm, observational wisdom)
  - *Calm expert analyst* (Tactical depth, field placements, bowling length)
  - *Sensational TV anchor* (High drama, explosive statements)
- **Natural Code-Mixing**: Preserves authentic cricket vernacular (*four, six, wicket, yorker, over*) in English within the Indic native script, just like real television broadcasts.
- **Synchronized Audio Queue**: Speaks each ball using Sarvam Text-to-Speech (`bulbul:v3`) with zero overlap, auto-advancing to the next ball when speech completes.
- **Live Stadium Scoreboard**: Visual score updates, overs counter, required run rate, active batter/bowler, and over balls tracker.
- **Zero Build Step**: Vanilla HTML5, CSS3, and modern JavaScript served directly by FastAPI.

---

## Architecture
- **Backend**: FastAPI (`main.py`)
  - `GET /`: Serves the frontend single-page application.
  - `GET /api/match`: Returns the hardcoded 3-over mini-match thriller (18 balls).
  - `POST /api/commentate`: Takes ball data, target language code, and persona.
    1. Prompts **Sarvam Chat** (`sarvam-105b` at `https://api.sarvam.ai/v1/chat/completions`) for commentary text.
    2. Prompts **Sarvam TTS** (`bulbul:v3` at `https://api.sarvam.ai/text-to-speech`) to generate base64-encoded WAV audio.
    3. Returns `{ text, audio_base64 }` to the client.
- **Frontend**: `static/index.html` (Stadium floodlight night theme, live scoreboard, audio queue player, and animated commentary stream).

---

## Quickstart & Run Commands

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `fastapi`, `uvicorn[standard]`, `httpx`, `python-dotenv`, `pydantic`)*

### 3. Configure `.env`
Ensure your Sarvam API Key is configured in `.env`:
```env
SARVAM_API_KEY=sk_mt9srfze_d9krZiqCGu2aBYdk6pxYVQQn
```

### 4. Run the Web Server
```bash
uvicorn main:app --reload --port 8000
```

### 5. Open in Browser
Open your browser and navigate to:
```
http://localhost:8000
```

Select your preferred language (e.g., Bengali) and persona, then click **Start Match** to experience the live broadcast!

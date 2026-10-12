import os
import logging
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("dhaaraa")

# Load environment variables
load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()
SARVAM_BASE_URL = "https://api.sarvam.ai"

app = FastAPI(title="Dhaaraa Commentary", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supported language codes to full names
LANGUAGE_MAP: Dict[str, str] = {
    "bn-IN": "Bengali",
    "hi-IN": "Hindi",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "gu-IN": "Gujarati",
    "pa-IN": "Punjabi",
    "en-IN": "English",
}

# High-stakes mini match (3 overs, 18 balls)
# Scenario: India chasing 185 against Pakistan, needing 33 runs from the final 18 balls.
HARDCODED_MATCH: List[Dict[str, Any]] = [
    # --- OVER 18 (Bowler: Haris Rauf) ---
    {
        "over": 18,
        "ball": 1,
        "bowler": "Haris Rauf",
        "batter": "Virat Kohli",
        "runs": 1,
        "event": "single",
        "score_so_far": 153,
        "wickets": 4,
        "description": "Kohli steers the 148 kmph delivery toward deep third man for a brisk single."
    },
    {
        "over": 18,
        "ball": 2,
        "bowler": "Haris Rauf",
        "batter": "Hardik Pandya",
        "runs": 0,
        "event": "dot",
        "score_so_far": 153,
        "wickets": 4,
        "description": "Fierce bouncer whistling past Pandya's helmet! Dot ball, high tension in the arena."
    },
    {
        "over": 18,
        "ball": 3,
        "bowler": "Haris Rauf",
        "batter": "Hardik Pandya",
        "runs": 4,
        "event": "four",
        "score_so_far": 157,
        "wickets": 4,
        "description": "Cracking shot! Pandya stands tall and punches it through extra cover for a blazing four!"
    },
    {
        "over": 18,
        "ball": 4,
        "bowler": "Haris Rauf",
        "batter": "Hardik Pandya",
        "runs": 1,
        "event": "single",
        "score_so_far": 158,
        "wickets": 4,
        "description": "Tucked off the hips toward deep square leg to bring Kohli back on strike."
    },
    {
        "over": 18,
        "ball": 5,
        "bowler": "Haris Rauf",
        "batter": "Virat Kohli",
        "runs": 6,
        "event": "six",
        "score_so_far": 164,
        "wickets": 4,
        "description": "Shot of the century! Back foot straight drive right back over Rauf's head into the stands for a monstrous six!"
    },
    {
        "over": 18,
        "ball": 6,
        "bowler": "Haris Rauf",
        "batter": "Virat Kohli",
        "runs": 1,
        "event": "single",
        "score_so_far": 165,
        "wickets": 4,
        "description": "Pushed softly to long-on to retain the strike. 13 runs scored from the 18th over!"
    },

    # --- OVER 19 (Bowler: Shaheen Afridi) ---
    {
        "over": 19,
        "ball": 1,
        "bowler": "Shaheen Afridi",
        "batter": "Virat Kohli",
        "runs": 1,
        "event": "single",
        "score_so_far": 166,
        "wickets": 4,
        "description": "Toe-crushing yorker from Shaheen, Kohli digs it out brilliantly to deep midwicket."
    },
    {
        "over": 19,
        "ball": 2,
        "bowler": "Shaheen Afridi",
        "batter": "Hardik Pandya",
        "runs": 0,
        "event": "wicket",
        "score_so_far": 166,
        "wickets": 5,
        "description": "OUT! Pandya goes for the big heave, miscues high into the night sky, and Babar takes the catch at long-on!"
    },
    {
        "over": 19,
        "ball": 3,
        "bowler": "Shaheen Afridi",
        "batter": "Dinesh Karthik",
        "runs": 0,
        "event": "dot",
        "score_so_far": 166,
        "wickets": 5,
        "description": "Beaten for pace! Karthik tries to dab it past backward point, misses completely."
    },
    {
        "over": 19,
        "ball": 4,
        "bowler": "Shaheen Afridi",
        "batter": "Dinesh Karthik",
        "runs": 1,
        "event": "single",
        "score_so_far": 167,
        "wickets": 5,
        "description": "Quick drop and run to cover! Dangerous single, direct hit missed!"
    },
    {
        "over": 19,
        "ball": 5,
        "bowler": "Shaheen Afridi",
        "batter": "Virat Kohli",
        "runs": 4,
        "event": "four",
        "score_so_far": 171,
        "wickets": 5,
        "description": "Pure artistry! Kohli opens the face of the bat and slices it between backward point and short third man for four!"
    },
    {
        "over": 19,
        "ball": 6,
        "bowler": "Shaheen Afridi",
        "batter": "Virat Kohli",
        "runs": 1,
        "event": "single",
        "score_so_far": 172,
        "wickets": 5,
        "description": "Squeezed to deep backward square leg. 13 runs needed off the final 6 balls!"
    },

    # --- OVER 20 (Bowler: Mohammad Nawaz) ---
    {
        "over": 20,
        "ball": 1,
        "bowler": "Mohammad Nawaz",
        "batter": "Virat Kohli",
        "runs": 1,
        "event": "single",
        "score_so_far": 173,
        "wickets": 5,
        "description": "Flatter delivery punched down to long-off for a single."
    },
    {
        "over": 20,
        "ball": 2,
        "bowler": "Mohammad Nawaz",
        "batter": "Dinesh Karthik",
        "runs": 0,
        "event": "wicket",
        "score_so_far": 173,
        "wickets": 6,
        "description": "WICKET! Karthik steps out, beaten in flight, and Rizwan whips off the bails in a flash!"
    },
    {
        "over": 20,
        "ball": 3,
        "bowler": "Mohammad Nawaz",
        "batter": "Ravichandran Ashwin",
        "runs": 1,
        "event": "wide",
        "score_so_far": 174,
        "wickets": 6,
        "description": "Fired down leg! Ashwin leaves it with immense composure, signaled wide by the umpire!"
    },
    {
        "over": 20,
        "ball": 4,
        "bowler": "Mohammad Nawaz",
        "batter": "Ravichandran Ashwin",
        "runs": 1,
        "event": "single",
        "score_so_far": 175,
        "wickets": 6,
        "description": "Lofted calmly over the infield to mid-off for a single! Kohli returns on strike with 10 needed!"
    },
    {
        "over": 20,
        "ball": 5,
        "bowler": "Mohammad Nawaz",
        "batter": "Virat Kohli",
        "runs": 6,
        "event": "six",
        "score_so_far": 181,
        "wickets": 6,
        "description": "UNBELIEVABLE! Kohli charges down and launches it over long-on for a gigantic six! Stadium erupts!"
    },
    {
        "over": 20,
        "ball": 6,
        "bowler": "Mohammad Nawaz",
        "batter": "Virat Kohli",
        "runs": 4,
        "event": "four",
        "score_so_far": 185,
        "wickets": 6,
        "description": "HE HAS DONE IT! Kohli lofts it over extra cover for four to seal a historic victory! Jubilation in the stands!"
    },
]


class BallData(BaseModel):
    over: int
    ball: int
    bowler: str
    batter: str
    runs: int
    event: str  # "dot", "single", "four", "six", "wicket", "wide"
    score_so_far: int
    wickets: int
    description: Optional[str] = None


class CommentateRequest(BaseModel):
    ball: BallData
    language_code: str
    persona: str


class CommentateResponse(BaseModel):
    text: str
    audio_base64: Optional[str] = None
    error: Optional[str] = None


@app.get("/api/match", response_model=List[Dict[str, Any]])
async def get_match():
    """Return the hardcoded mini-match balls sequence."""
    return HARDCODED_MATCH


@app.post("/api/commentate", response_model=CommentateResponse)
async def commentate(request: CommentateRequest):
    """
    1. Prompt Sarvam Chat LLM (sarvam-105b) for commentary text.
    2. Convert text to speech using Sarvam TTS (bulbul:v3).
    3. Return text and base64 audio.
    """
    api_key = os.getenv("SARVAM_API_KEY", "").strip() or SARVAM_API_KEY
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="SARVAM_API_KEY not configured. Please set SARVAM_API_KEY in .env file."
        )

    lang_name = LANGUAGE_MAP.get(request.language_code, "Bengali")
    ball_dict = request.ball.model_dump()

    # Exact required system prompt
    system_prompt = (
        f"You are a live cricket commentator. Persona: {request.persona}. "
        f"Respond ONLY in {lang_name}, in its native script. "
        f"Write 1-2 short, vivid, emotional sentences about the ball just bowled. "
        f"Keep English cricket terms (four, six, wicket, yorker, over) in English "
        f"the way Indian commentators naturally do. Mention player names. "
        f"Match the energy to the event: a six or wicket should sound explosive, a dot ball calm and tense. "
        f"No emojis, no hashtags, no explanations."
    )

    user_prompt = (
        f"Over {ball_dict['over']}.{ball_dict['ball']} bowled by {ball_dict['bowler']} to {ball_dict['batter']}. "
        f"Event: {ball_dict['event'].upper()}. Runs on this ball: {ball_dict['runs']}. "
        f"Current match score: {ball_dict['score_so_far']}/{ball_dict['wickets']}. "
        f"Action detail: {ball_dict.get('description', '')}"
    )

    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json",
    }

    commentary_text = ""
    audio_base64 = None
    generation_error = None

    # Step 1: Call Sarvam Chat Completion
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            chat_url = f"{SARVAM_BASE_URL}/v1/chat/completions"
            chat_payload = {
                "model": "sarvam-105b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "reasoning_effort": None,
                "max_tokens": 300,
            }
            logger.info("Calling Sarvam Chat Completion (%s, %s)...", lang_name, request.persona)
            chat_resp = await client.post(chat_url, json=chat_payload, headers=headers)
            
            if chat_resp.status_code == 200:
                chat_data = chat_resp.json()
                choices = chat_data.get("choices", [])
                if choices and "message" in choices[0]:
                    raw_content = choices[0]["message"].get("content")
                    if raw_content:
                        commentary_text = raw_content.strip()
            
            # If content was empty, fallback to sarvam-105b-conversations
            if not commentary_text:
                logger.info("Falling back to sarvam-105b-conversations...")
                chat_payload["model"] = "sarvam-105b-conversations"
                chat_payload.pop("reasoning_effort", None)
                chat_resp = await client.post(chat_url, json=chat_payload, headers=headers)
                if chat_resp.status_code == 200:
                    chat_data = chat_resp.json()
                    choices = chat_data.get("choices", [])
                    if choices and "message" in choices[0]:
                        raw_content = choices[0]["message"].get("content")
                        if raw_content:
                            commentary_text = raw_content.strip()
            
            if not commentary_text and chat_resp.status_code != 200:
                logger.error("Sarvam Chat Error %d: %s", chat_resp.status_code, chat_resp.text)
                generation_error = f"Chat API returned {chat_resp.status_code}: {chat_resp.text}"
        except Exception as e:
            logger.exception("Failed to call Sarvam Chat API: %s", e)
            generation_error = f"Chat call failed: {str(e)}"

        # Fallback text if LLM call failed
        if not commentary_text:
            commentary_text = f"Over {ball_dict['over']}.{ball_dict['ball']}: {ball_dict['bowler']} to {ball_dict['batter']}, {ball_dict['event']}! ({ball_dict.get('description', '')})"

        # Step 2: Call Sarvam Text-to-Speech
        try:
            tts_url = f"{SARVAM_BASE_URL}/text-to-speech"
            tts_payload = {
                "text": commentary_text,
                "language_code": request.language_code,
                "model": "bulbul:v3",
                "speaker": "shubh",
            }
            logger.info("Calling Sarvam TTS (%s)...", request.language_code)
            tts_resp = await client.post(tts_url, json=tts_payload, headers=headers)
            
            if tts_resp.status_code == 200:
                tts_data = tts_resp.json()
                audios = tts_data.get("audios", [])
                if audios:
                    audio_base64 = audios[0]
            else:
                logger.error("Sarvam TTS Error %d: %s", tts_resp.status_code, tts_resp.text)
                if not generation_error:
                    generation_error = f"TTS API returned {tts_resp.status_code}: {tts_resp.text}"
        except Exception as e:
            logger.exception("Failed to call Sarvam TTS API: %s", e)
            if not generation_error:
                generation_error = f"TTS call failed: {str(e)}"

    return CommentateResponse(
        text=commentary_text,
        audio_base64=audio_base64,
        error=generation_error
    )


# Static files mount and root route
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Dhaaraa Commentary Backend Running. static/index.html not found."}

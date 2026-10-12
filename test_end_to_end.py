import asyncio
import os
import sys
import httpx
from dotenv import load_dotenv

# Ensure utf-8 stdout in windows console
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv("C:/Users/rijup/.gemini/antigravity/scratch/dhaaraa-commentary/.env")
api_key = os.getenv("SARVAM_API_KEY", "")

headers = {
    "api-subscription-key": api_key,
    "Content-Type": "application/json"
}

system_prompt = (
    "You are a live cricket commentator. Persona: Excited fan. "
    "Respond ONLY in Bengali, in its native script. Write 1-2 short, vivid, emotional sentences about the ball just bowled. "
    "Keep English cricket terms (four, six, wicket, yorker, over) in English the way Indian commentators naturally do. "
    "Mention player names. Match the energy to the event: a six or wicket should sound explosive, a dot ball calm and tense. "
    "No emojis, no hashtags, no explanations."
)

user_prompt = "Over 18.5 bowled by Haris Rauf to Virat Kohli. Event: SIX. Runs on this ball: 6. Current match score: 164/4. Action detail: Shot of the century! Back foot straight drive right back over Rauf's head into the stands for a monstrous six!"

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Chat
        print("1. Testing Chat Completion with max_tokens=500...")
        chat_resp = await client.post("https://api.sarvam.ai/v1/chat/completions", json={
            "model": "sarvam-105b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }, headers=headers)
        
        chat_data = chat_resp.json()
        content = chat_data["choices"][0]["message"]["content"]
        print("Generated Bengali Text:\n", content)
        
        # Step 2: TTS
        print("\n2. Testing TTS with generated Bengali text...")
        tts_resp = await client.post("https://api.sarvam.ai/text-to-speech", json={
            "text": content,
            "language_code": "bn-IN",
            "model": "bulbul:v3",
            "speaker": "shubh"
        }, headers=headers)
        
        print("TTS Status:", tts_resp.status_code)
        if tts_resp.status_code == 200:
            tts_data = tts_resp.json()
            audios = tts_data.get("audios", [])
            print("Received audios count:", len(audios))
            if audios:
                print("Base64 audio length:", len(audios[0]))
                import base64
                audio_bytes = base64.b64decode(audios[0])
                with open("C:/Users/rijup/.gemini/antigravity/scratch/dhaaraa-commentary/test_bengali.wav", "wb") as f:
                    f.write(audio_bytes)
                print("Saved audio file test_bengali.wav (size:", len(audio_bytes), "bytes) - SUCCESS!")
        else:
            print("TTS Error:", tts_resp.text)

asyncio.run(main())

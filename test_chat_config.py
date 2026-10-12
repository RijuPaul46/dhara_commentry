import asyncio
import os
import httpx
from dotenv import load_dotenv

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

async def test_config(name, payload):
    print(f"\n--- Testing: {name} ---")
    async with httpx.AsyncClient(timeout=30.0) as client:
        chat_resp = await client.post("https://api.sarvam.ai/v1/chat/completions", json=payload, headers=headers)
        print("Status:", chat_resp.status_code)
        if chat_resp.status_code == 200:
            data = chat_resp.json()
            choice = data["choices"][0]
            print("Finish reason:", choice.get("finish_reason"))
            print("Reasoning content:", choice.get("message", {}).get("reasoning_content")[:60] if choice.get("message", {}).get("reasoning_content") else None)
            print("Content:", choice.get("message", {}).get("content"))
            return choice.get("message", {}).get("content")
        else:
            print("Error:", chat_resp.text)
            return None

async def main():
    # Test 1: max_tokens = 500
    res1 = await test_config("max_tokens=500", {
        "model": "sarvam-105b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    })

    # Test 2: reasoning_effort = None, max_tokens = 500
    res2 = await test_config("reasoning_effort=None", {
        "model": "sarvam-105b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "reasoning_effort": None,
        "max_tokens": 500
    })

    # Test 3: sarvam-105b-conversations
    res3 = await test_config("model=sarvam-105b-conversations", {
        "model": "sarvam-105b-conversations",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    })

asyncio.run(main())

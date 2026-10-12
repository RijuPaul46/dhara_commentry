import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv("C:/Users/rijup/.gemini/antigravity/scratch/dhaaraa-commentary/.env")
api_key = os.getenv("SARVAM_API_KEY", "")

print("Testing Sarvam API directly with Bengali (bn-IN)...")
print("API Key present:", bool(api_key), f"Length: {len(api_key)}")

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

async def run():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test Chat
        chat_url = "https://api.sarvam.ai/v1/chat/completions"
        chat_payload = {
            "model": "sarvam-105b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        print("Sending request to Sarvam Chat...")
        chat_resp = await client.post(chat_url, json=chat_payload, headers=headers)
        print("Chat response status:", chat_resp.status_code)
        print("Chat response body:", chat_resp.text)
        
        if chat_resp.status_code != 200:
            print("Chat failed!")
            return
            
        commentary = chat_resp.json()["choices"][0]["message"]["content"]
        print("\nGenerated Bengali commentary:\n", commentary)

        # Test TTS
        tts_url = "https://api.sarvam.ai/text-to-speech"
        tts_payload = {
            "text": commentary,
            "language_code": "bn-IN",
            "model": "bulbul:v3",
            "speaker": "shubh"
        }
        print("\nSending request to Sarvam TTS...")
        tts_resp = await client.post(tts_url, json=tts_payload, headers=headers)
        print("TTS response status:", tts_resp.status_code)
        if tts_resp.status_code == 200:
            data = tts_resp.json()
            audios = data.get("audios", [])
            print("Audio received! Number of clips:", len(audios))
            if audios:
                print("Audio b64 length:", len(audios[0]))
                # Save audio to file to verify
                import base64
                audio_bytes = base64.b64decode(audios[0])
                with open("C:/Users/rijup/.gemini/antigravity/scratch/dhaaraa-commentary/test_output.wav", "wb") as f:
                    f.write(audio_bytes)
                print("Saved audio to test_output.wav (size:", len(audio_bytes), "bytes)")
        else:
            print("TTS response error:", tts_resp.text)

asyncio.run(run())

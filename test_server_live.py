import sys
import httpx

sys.stdout.reconfigure(encoding='utf-8')

def test():
    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=35.0)
    
    # 1. Test GET /
    print("Testing GET / ...")
    r0 = client.get("/")
    print("Root status:", r0.status_code, "Length:", len(r0.text))
    assert r0.status_code == 200
    assert "Dhaaraa Commentary" in r0.text
    
    # 2. Test GET /api/match
    print("\nTesting GET /api/match ...")
    r1 = client.get("/api/match")
    print("Match status:", r1.status_code)
    balls = r1.json()
    print("Total balls:", len(balls))
    assert r1.status_code == 200
    assert len(balls) == 18
    print("First ball:", balls[0])
    
    # 3. Test POST /api/commentate with Bengali (bn-IN) and Excited fan
    print("\nTesting POST /api/commentate (Bengali, Excited fan)...")
    payload = {
        "ball": balls[0],
        "language_code": "bn-IN",
        "persona": "Excited fan"
    }
    r2 = client.post("/api/commentate", json=payload)
    print("Commentate status:", r2.status_code)
    assert r2.status_code == 200
    res = r2.json()
    print("Commentary Text:\n", res.get("text"))
    audio_b64 = res.get("audio_base64")
    print("Audio B64 present:", bool(audio_b64))
    if audio_b64:
        print("Audio B64 length:", len(audio_b64))
    print("Error:", res.get("error"))
    print("\nALL BACKEND & END-TO-END TESTS PASSED!")

if __name__ == "__main__":
    test()

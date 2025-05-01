import httpx

payload = {"url": "http://localhost:3000/webhook", "event": "payment_received"}

response = httpx.post("http://127.0.0.1:5000/webhooks/register", json=payload)

print(f"✅ Register response: {response.status_code} {response.text}")

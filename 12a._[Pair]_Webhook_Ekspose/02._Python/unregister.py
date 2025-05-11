import httpx
from typing import Any

payload = {"url": "http://localhost:3000/webhook", "event": "payment_received"}

response = httpx.request(
    method="DELETE",
    url="http://127.0.0.1:5000/webhooks/unregister",
    json=payload,  # Safe because request() accepts JSON
)

print(f"🗑️ Unregister response: {response.status_code} {response.text}")

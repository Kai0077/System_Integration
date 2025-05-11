from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, AnyHttpUrl, constr
import json
import os
import requests

app = FastAPI()
WEBHOOK_FILE = "webhooks.json"

ALLOWED_EVENTS = {
    "payment_received",
    "payment_processed",
    "invoice_processing",
    "invoice_completed",
}

if os.path.exists(WEBHOOK_FILE):
    try:
        with open(WEBHOOK_FILE, "r") as f:
            content = f.read().strip()
            webhooks = json.loads(content) if content else []
    except json.JSONDecodeError:
        webhooks = []
else:
    webhooks = []


def save_webhooks():
    with open(WEBHOOK_FILE, "w") as f:
        json.dump(webhooks, f, indent=2)


class WebhookRequest(BaseModel):
    url: AnyHttpUrl
    event: constr(strip_whitespace=True, min_length=1)  # type: ignore


class EventTrigger(BaseModel):
    event: str
    data: dict


@app.post("/webhooks/register")
def register_webhook(req: WebhookRequest):
    if req.event not in ALLOWED_EVENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid event. Allowed: {', '.join(ALLOWED_EVENTS)}",
        )

    if any(w["url"] == req.url and w["event"] == req.event for w in webhooks):
        raise HTTPException(status_code=409, detail="Webhook already registered")

    webhooks.append(jsonable_encoder(req))
    save_webhooks()
    return {"message": "Webhook registered"}


@app.delete("/webhooks/unregister")
def unregister_webhook(
    req: WebhookRequest = Body(...),
):  # ✅ Body is required for DELETE
    global webhooks
    initial_len = len(webhooks)

    webhooks = [
        w for w in webhooks if not (w["url"] == req.url and w["event"] == req.event)
    ]

    removed_count = initial_len - len(webhooks)
    save_webhooks()

    if removed_count == 0:
        raise HTTPException(status_code=404, detail="Webhook not found")

    return {"message": f"{removed_count} webhook(s) unregistered"}


@app.get("/ping")
def ping_all():
    for wh in webhooks:
        try:
            requests.post(
                wh["url"], json={"event": "ping", "data": "Ping from Exposee"}
            )
        except Exception as e:
            print(f"⚠️ Failed to ping {wh['url']}: {e}")
    return {"message": "Ping sent"}


@app.post("/trigger")
def trigger_event(payload: EventTrigger):
    if payload.event not in ALLOWED_EVENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid event. Allowed: {', '.join(ALLOWED_EVENTS)}",
        )

    sent = 0
    for wh in webhooks:
        if wh["event"] == payload.event:
            try:
                requests.post(
                    wh["url"], json={"event": payload.event, "data": payload.data}
                )
                sent += 1
            except Exception as e:
                print(f"⚠️ Failed to send to {wh['url']}: {e}")
    return {"message": f"Event '{payload.event}' triggered to {sent} webhook(s)"}

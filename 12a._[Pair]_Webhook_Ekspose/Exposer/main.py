from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, AnyHttpUrl
from typing import List
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


def normalize_url(url: str) -> str:
    return url.rstrip("/").lower()


def normalize_event(event: str) -> str:
    return event.strip().lower()


class WebhookRequest(BaseModel):
    url: AnyHttpUrl
    event: str


class WebhookMultiRequest(BaseModel):
    url: AnyHttpUrl
    event_types: List[str]


@app.post("/webhooks/register")
def register_webhook(req: WebhookMultiRequest):
    for event in req.event_types:
        if event not in ALLOWED_EVENTS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event '{event}'. Allowed: {', '.join(ALLOWED_EVENTS)}",
            )

    for event in req.event_types:
        if any(w["url"] == str(req.url) and w["event"] == event for w in webhooks):
            continue
        webhooks.append(jsonable_encoder({"url": str(req.url), "event": event}))

    save_webhooks()
    return {"message": f"Webhook registered for: {', '.join(req.event_types)}"}


@app.delete("/webhooks/unregister")
def unregister_webhook(req: WebhookRequest = Body(...)):
    global webhooks

    req_url = normalize_url(str(req.url))
    req_event = normalize_event(req.event)

    initial_len = len(webhooks)
    webhooks = [
        w
        for w in webhooks
        if not (
            normalize_url(w["url"]) == req_url
            and normalize_event(w["event"]) == req_event
        )
    ]

    removed_count = initial_len - len(webhooks)
    save_webhooks()

    if removed_count == 0:
        raise HTTPException(status_code=404, detail="Webhook not found")

    return {"message": f"{removed_count} webhook(s) unregistered"}


@app.get("/ping")
def ping_all():
    for wh in webhooks:
        payload = {"event": "ping", "data": "Ping from Exposee"}
        try:
            requests.post(wh["url"], json=payload)
        except Exception:
            pass
    return {"message": "Ping sent"}

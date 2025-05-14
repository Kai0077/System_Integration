from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, AnyHttpUrl, constr
from typing import List, Dict
from datetime import datetime
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

# Load or initialize webhooks
if os.path.exists(WEBHOOK_FILE):
    try:
        with open(WEBHOOK_FILE, "r") as f:
            content = f.read().strip()
            webhooks = json.loads(content) if content else []
    except json.JSONDecodeError:
        webhooks = []
else:
    webhooks = []

# Stores last ping payload sent to each URL
last_ping_payloads = {}


def save_webhooks():
    with open(WEBHOOK_FILE, "w") as f:
        json.dump(webhooks, f, indent=2)


def normalize_url(url: str) -> str:
    return url.rstrip("/").lower()


def normalize_event(event: str) -> str:
    return event.strip().lower()


def send_webhook(url: str, payload: dict):
    print(f"📡 Sending webhook to {url} for event '{payload['event_type']}'")
    try:
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}, timeout=5
        )
        response.raise_for_status()
        print(f"✅ Webhook sent successfully to {url}")
    except requests.RequestException as e:
        print(
            f"❌ Failed to send webhook to {url} for event '{payload['event_type']}': {e}"
        )


class WebhookRequest(BaseModel):
    url: AnyHttpUrl
    event: constr(strip_whitespace=True, min_length=1)  # type: ignore


class EventTrigger(BaseModel):
    event: str
    data: dict


class NamedEventRequest(BaseModel):
    event_type: str
    data: dict


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
        if any(w["url"] == req.url and w["event"] == event for w in webhooks):
            continue  # skip if already registered

        webhooks.append(jsonable_encoder({"url": req.url, "event": event}))

    save_webhooks()
    return {"message": f"Webhook registered for: {', '.join(req.event_types)}"}


@app.delete("/webhooks/unregister")
def unregister_webhook(req: WebhookRequest = Body(...)):
    global webhooks

    req_url = normalize_url(str(req.url))  # 👈 fix here
    req_event = normalize_event(req.event)

    print(f"📤 Unregistering webhook for: {req_url} / {req_event}")

    for w in webhooks:
        print(f"🔍 Existing: {w['url']} / {w['event']}")

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
    global last_ping_payloads
    for wh in webhooks:
        payload = {"event": "ping", "data": "Ping from Exposeeeeeeee"}
        last_ping_payloads[wh["url"]] = payload
        try:
            requests.post(wh["url"], json=payload)
            print(f"✅ Sent ping to {wh['url']}")
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


@app.post("/event")
def trigger_named_event(payload: NamedEventRequest):
    event_type = payload.event_type
    data = payload.data

    print(f"[Exposee] Event '{event_type}'.")

    sent = 0
    for webhook in webhooks:
        subscribed_events = webhook.get("event_types")
        if isinstance(subscribed_events, list) and event_type in subscribed_events:
            event_payload = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data,
            }
            send_webhook(webhook["url"], event_payload)
            sent += 1

    return {"message": f"Event '{event_type}' triggered for {sent} webhook(s)."}


@app.post("/webhooks/ping-back")
async def receive_ping_from_registered(req: Request):
    try:
        data = await req.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    sender_url = data.get("url")
    if not sender_url:
        raise HTTPException(status_code=400, detail="Missing 'url' in payload")

    # Check if the sender URL is registered
    matching_webhook = next((w for w in webhooks if w["url"] == sender_url), None)
    if not matching_webhook:
        raise HTTPException(status_code=404, detail="Webhook not registered")

    original_ping = last_ping_payloads.get(sender_url)
    if not original_ping:
        return {"message": "Ping received, but no original ping found"}

    print(f"✅ Received ping-back from {sender_url}")
    return original_ping

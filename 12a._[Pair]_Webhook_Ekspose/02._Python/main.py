from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import requests

app = FastAPI()
WEBHOOK_FILE = "webhooks.json"

# Load or create webhook store
if os.path.exists(WEBHOOK_FILE):
    with open(WEBHOOK_FILE, "r") as f:
        webhooks = json.load(f)
else:
    webhooks = []


def save_webhooks():
    with open(WEBHOOK_FILE, "w") as f:
        json.dump(webhooks, f, indent=2)


class WebhookRequest(BaseModel):
    url: str
    event: str


class EventTrigger(BaseModel):
    event: str
    data: dict


@app.post("/webhooks/register")
def register_webhook(req: WebhookRequest):
    webhooks.append(req.dict())
    save_webhooks()
    return {"message": "Webhook registered"}


@app.delete("/webhooks/unregister")
def unregister_webhook(req: WebhookRequest):
    global webhooks
    webhooks = [
        w for w in webhooks if not (w["url"] == req.url and w["event"] == req.event)
    ]
    save_webhooks()
    return {"message": "Webhook unregistered"}


@app.get("/ping")
def ping_all():
    for wh in webhooks:
        requests.post(wh["url"], json={"event": "ping", "data": "Ping from Exposee"})
    return {"message": "Ping sent"}


@app.post("/trigger")
def trigger_event(payload: EventTrigger):
    for wh in webhooks:
        if wh["event"] == payload.event:
            requests.post(
                wh["url"], json={"event": payload.event, "data": payload.data}
            )
    return {"message": f"Event '{payload.event}' triggered"}

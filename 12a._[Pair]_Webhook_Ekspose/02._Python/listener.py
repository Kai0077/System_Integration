from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print(f"📬 Webhook received: {data}")
    return {"message": "Received"}

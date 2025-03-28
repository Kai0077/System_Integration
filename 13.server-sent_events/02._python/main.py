import random
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from fastapi.responses import PlainTextResponse
from datetime import datetime
import asyncio

app = FastAPI()


templates = Jinja2Templates(directory="templates")

## skriv lt --port 8000 -s kaizen og uvicorn main:app --reload så det virker og brug endpointet


@app.get("/hola")
def save_root_page(request: Request):
    print("hej")
    return templates.TemplateResponse("index.html", {"request": request})


messages = ["hej", "Hello!", "Hi there!", "Greetings!", "Salutations!"]


@app.get("/random", response_class=PlainTextResponse)
async def random_message():
    return random.choice(messages)


async def date_generator():
    while True:
        now = datetime.now().strftime("%Y-%m%dT%H:%M:%S")
        yield f"data:{now}\n\n"
        await asyncio.sleep(1)


@app.get("/sse")
def sse():
    return StreamingResponse(date_generator(), media_type="text/event-stream")

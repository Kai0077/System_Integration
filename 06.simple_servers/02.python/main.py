from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/greet")
def greet():
    return {"message": f"Hello there "}

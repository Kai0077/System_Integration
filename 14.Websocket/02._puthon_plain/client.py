from websockets.sync.client import connect


def send_message():
    with connect("ws://localhost:8000") as websocket:
        websocket.send("hello")

        message = websocket.recv()
        print(f"received: {message}")

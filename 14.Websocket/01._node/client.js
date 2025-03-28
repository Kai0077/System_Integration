import { WebSocket } from "ws";

const WebSocketClient = new WebSocket("ws://localhost:8080");

WebSocketClient.on('open', () => {
    WebSocketClient.send("sending a client message from node.js");

    WebSocketClient.on("message", (message) => {
        console.log(`Received a message from the server: ${message}`)
    })
})
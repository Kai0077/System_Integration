import express from 'express';

const app = express();

app.use(express.static("public"));

app.get("/synchronizetime", (req, res) => {
    res.writeHead(200, {
        "Connectioin": "keep-alive",
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
    });

    setInterval(() => sendTimeToClient(res), 1000);
});


function sendTimeToClient(res) {
    const time = new Date().toISOString();
    res.write(`data: ${time} \n\n`);
    // to send data you have to write data:, and it works with eventsource in the frontend 
}

const PORT = Number(process.env.PORT) || 8080;
app.listen(PORT, () => console.log("Server stated on port", PORT));

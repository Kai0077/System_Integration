import express from 'express';

const app = express();

let clients = [];

app.get("/events/subscribe", (req, res) => {
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.flushHeaders();

    clients.push(res);

    req.on('close', () => {
        clients = clients.filter((client) => client !== res);
    });

});

app.get("/events/publish", (req, res) => {
    const message = {data: "Hello!"};

    clients.forEach((client) => {
        client.write(`data: ${JSON.stringify(message)}\n\n`);
    });

    clients = [];

    res.status(204).end();
});


const PORT = 8080;  
app.listen(PORT, () => console.log("Server stated on port", PORT));


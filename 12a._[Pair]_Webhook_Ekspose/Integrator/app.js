import express from 'express';

const app = express();
app.use(express.json());

app.post("/webhook-receiver", (req, res) => {
    console.log("Received webhook payload:", req.body);
    res.sendStatus(204);
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(" Webhook listener running on port", PORT);
});
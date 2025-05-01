import express from 'express';
const app = express();

app.use(express.json());

app.post("/githubwebhookjson", (req, res) => {
    console.log(req.body);
    res.sendStatus(204);
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, console.log("server is running on ", PORT ));
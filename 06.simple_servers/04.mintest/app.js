import express from 'express';

const app = express();

app.get('/', (req, res) => {
    res.send('hahahahahahhahahahahahhahahaha');
});

const PORT = 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
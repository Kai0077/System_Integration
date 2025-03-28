import express from 'express';

const app = express(); 



app.get('/greetings', (req, res) => {
    res.send("Salutations sir");
});

app.listen(8080, () => console.log('Server running on port 8080'));

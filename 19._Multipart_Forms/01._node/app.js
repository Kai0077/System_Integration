import express from 'express'

const app = express();

app.use(express.urlencoded({extended:true}))

import multer from 'multer';
const upload = multer({dest: 'uploads/'})

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(undefined, './upload');
    },
    filename: (req, file, cb) => {
        console.log(file.originalname);

        cb(undefined, "")
    }
})

app.post("/form", (req, res) => {
    console.log(req.body);
    delete req.body.password;
    res.send(req.body)
});

app.post("/fileform", upload.single('file'), (req, res) => {
    console.log(req.body);
    req.send();

})

const PORT = Number(process.env.PORT) || 8080;
app.listen(PORT,() => console.log("server is running on port", PORT));
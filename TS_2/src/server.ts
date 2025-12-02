import express, { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, '..')));
app.use(express.json({ limit: '10mb' }));

app.post('/save', (req: Request, res: Response) => {
    const { image } = req.body;
    const base64Data = image.replace(/^data:image\/png;base64,/, "");
    const imageName = `drawing-${Date.now()}.png`;
    const imagePath = path.join(__dirname, '..', 'img', imageName);

    fs.writeFile(imagePath, base64Data, 'base64', (err) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to save image' });
        }
        res.json({ message: 'Image saved successfully' });
    });
});

app.get('/images', (req: Request, res: Response) => {
    const imgDir = path.join(__dirname, '..', 'img');
    fs.readdir(imgDir, (err, files) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to read images' });
        }
        res.json(files);
    });
});

app.delete('/images/:filename', (req: Request, res: Response) => {
    const { filename } = req.params;
    const imagePath = path.join(__dirname, '..', 'img', filename);

    fs.unlink(imagePath, (err) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to delete image' });
        }
        res.json({ message: 'Image deleted sucessfully' });
    });
});

//
app.delete('/images', (req: Request, res: Response) => {
    const imgDir = path.join(__dirname, '..', 'img');

    fs.readdir(imgDir, (err, files) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to read images' });
        }

        // Удаляем все файлы
        for (const file of files) {
            fs.unlinkSync(path.join(imgDir, file));
        }

        res.json({ message: 'All images deleted successfully' });
    });
});
//



app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});

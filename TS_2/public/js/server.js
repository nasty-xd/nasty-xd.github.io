"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const app = (0, express_1.default)();
const port = 3000;
app.use(express_1.default.static(path_1.default.join(__dirname, '..')));
app.use(express_1.default.json({ limit: '10mb' }));
app.post('/save', (req, res) => {
    const { image } = req.body;
    const base64Data = image.replace(/^data:image\/png;base64,/, "");
    const imageName = `drawing-${Date.now()}.png`;
    const imagePath = path_1.default.join(__dirname, '..', 'img', imageName);
    fs_1.default.writeFile(imagePath, base64Data, 'base64', (err) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to save image' });
        }
        res.json({ message: 'Image saved successfully' });
    });
});
app.get('/images', (req, res) => {
    const imgDir = path_1.default.join(__dirname, '..', 'img');
    fs_1.default.readdir(imgDir, (err, files) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to read images' });
        }
        res.json(files);
    });
});
app.delete('/images/:filename', (req, res) => {
    const { filename } = req.params;
    const imagePath = path_1.default.join(__dirname, '..', 'img', filename);
    fs_1.default.unlink(imagePath, (err) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to delete image' });
        }
        res.json({ message: 'Image deleted sucessfully' });
    });
});
app.delete('/images', (req, res) => {
    const imgDir = path_1.default.join(__dirname, '..', 'img');
    fs_1.default.readdir(imgDir, (err, files) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Failed to read images' });
        }
        // Удаляем все файлы
        for (const file of files) {
            fs_1.default.unlinkSync(path_1.default.join(imgDir, file));
        }
        res.json({ message: 'All images deleted successfully' });
    });
});
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});

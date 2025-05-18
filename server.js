const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static files (CSS, images, etc.)
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'HomePage.html'));
});

app.post('/talk-to-ai', (req, res) => {
    // Replace this logic with actual processing if needed
    console.log("Button clicked - talk to AI");
    res.redirect('/');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

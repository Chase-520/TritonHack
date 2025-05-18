const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer(); // store files in memory for now

app.use(express.static(path.join(__dirname, 'public')));

// POST endpoint for audio from frontend mic recorder
app.post('/talk_to_ai', upload.single('audio'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No audio file received' });
  }

  // Write audio buffer to temp file
  const tempFilePath = path.join(__dirname, 'temp_audio.webm');
  fs.writeFileSync(tempFilePath, req.file.buffer);

  // Call python script with temp file path
  const pythonProcess = spawn('python3', ['python_script.py', tempFilePath]);

  let pythonOutput = '';
  let pythonError = '';

  pythonProcess.stdout.on('data', (data) => {
    pythonOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    pythonError += data.toString();
  });

  pythonProcess.on('close', (code) => {
    // Clean up temp file
    fs.unlinkSync(tempFilePath);

    if (code === 0) {
      res.json({ message: pythonOutput.trim() || 'Processing complete' });
    } else {
      console.error('Python script error:', pythonError);
      res.status(500).json({ message: 'Python processing error' });
    }
  });
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server listening on http://localhost:${PORT}`));

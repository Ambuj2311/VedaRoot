const express = require('express');
const cors = require('cors');
const path = require('path');
const fileUpload = require('express-fileupload');
const axios = require('axios');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(fileUpload());

// API endpoint for plant prediction
app.post('/api/predict', async (req, res) => {
  try {
    if (!req.files || !req.files.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const file = req.files.file;
    
    // Forward to Flask backend
    const formData = new FormData();
    formData.append('file', file.data, {
      filename: file.name,
      contentType: file.mimetype
    });

    const flaskResponse = await axios.post('http://localhost:5000/predict', formData, {
      headers: {
        ...formData.getHeaders(),
        'Content-Type': 'multipart/form-data'
      }
    });

    res.json(flaskResponse.data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Serve your React app routes
app.get('/', (req, res) => {
  res.send('Welcome to Vedaroot Medicinal Plant Detection');
});

app.get('/upload', (req, res) => {
  res.send('Upload page would be served here');
});

app.get('/results', (req, res) => {
  res.send('Results page would be served here');
});

// Error handling for undefined routes
app.use((req, res) => {
  res.status(404).send('Route not found');
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
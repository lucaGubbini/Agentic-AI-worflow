require('dotenv').config();
const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');
const helmet = require('helmet');
const fs = require('fs');
const https = require('https');
const path = require('path');
const http = require('http'); // Make sure to require the http module

const app = express();
const port = process.env.PORT || 8001;
const mongoUri = process.env.MONGO_URI;

let dbClient;
let db;

async function connectToDatabase() {
    if (!dbClient) {
        dbClient = new MongoClient(mongoUri);
        await dbClient.connect();
        db = dbClient.db('chatApp');
        console.log('Connected successfully to database');
    }
}


// Middleware
app.use(cors({ origin: process.env.CORS_ORIGIN || '*' }));
app.use(helmet());
app.use(express.json());
app.use(express.static('public', { maxAge: '1d' }));

// Route handlers
app.get('/', async (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/agent-setup', async (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'agentSetup.html'));
});

// Code generation route with MongoDB integration
app.post('/generate-code', async (req, res) => {
    const { description, sessionId } = req.body;
    if (!description || !sessionId) {
        return res.status(400).json({ error: 'Description and Session ID are required.' });
    }

    // Example logic to generate code
    const generatedCode = `Code for ${description}`;

    try {
        await db.collection('generatedCodes').insertOne({ sessionId, description, generatedCode, createdAt: new Date() });
        res.json({ generatedCode });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to save generated code.' });
    }
});

// Agent creation route
app.post('/create-agent', async (req, res) => {
    const agentData = req.body;

    try {
        const result = await db.collection('agents').insertOne({ ...agentData, createdAt: new Date() });
        res.status(201).json({ message: 'Agent created successfully', agentId: result.insertedId });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to create agent.' });
    }
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
});

// Server initialization
async function startServer() {
    await connectToDatabase();
    let server;

    if (process.env.USE_HTTPS === 'true') {
        try {
            const httpsOptions = {
                key: fs.readFileSync(path.resolve(process.env.SSL_KEY_PATH)),
                cert: fs.readFileSync(path.resolve(process.env.SSL_CERT_PATH)),
            };
            server = https.createServer(httpsOptions, app);
            console.log(`HTTPS server starting on port ${port}`);
        } catch (error) {
            console.warn('SSL setup failed. Falling back to HTTP:', error.message);
            server = http.createServer(app); // Fallback to HTTP if SSL setup fails
        }
    } else {
        console.log('Starting HTTP server (HTTPS disabled or SSL files not found).');
        server = http.createServer(app); // Explicitly use HTTP if USE_HTTPS is false
    }

    server.listen(port, () => {
        console.log(`Server running at http${process.env.USE_HTTPS === 'true' ? 's' : ''}://localhost:${port}`);
    });
}

startServer();

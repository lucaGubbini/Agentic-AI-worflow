const express = require('express');
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 8001;
const mongoUri = 'mongodb://localhost:27017/chatApp';

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

let dbClient;

async function connectToDatabase() {
    if (!dbClient) {
        dbClient = new MongoClient(mongoUri);
        await dbClient.connect();
        console.log('Connected successfully to database');
    }
    return dbClient.db('chatApp').collection('chats');
}

app.post('/generate-code', async (req, res) => {
    try {
        const chats = await connectToDatabase();
        const { description, sessionId } = req.body;
        if (!description) {
            return res.status(400).json({ error: 'Description is required.' });
        }

        // Placeholder logic to fetch data from the database that influences code generation
        const dbDataUsed = await chats.find({ sessionId }).toArray();
        const influencedByDbData = dbDataUsed.length > 0;

        const generatedCode = `Code based on: ${description}`; // Placeholder logic
        await chats.insertOne({ sessionId, prompt: description, response: generatedCode });

        res.json({
            code: generatedCode,
            influencedByDbData,
            dbDataDetails: influencedByDbData ? dbDataUsed : []
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while generating code.' });
    }
});

app.post('/save-chat', async (req, res) => {
    try {
        const chats = await connectToDatabase();
        const { chatHistory } = req.body;
        await chats.insertOne({ chatHistory, timestamp: new Date() });
        res.json({ message: 'Chat history saved successfully.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while saving chat history.' });
    }
});

app.post('/save-message', async (req, res) => {
    try {
        const chats = await connectToDatabase();
        const { sessionId, message } = req.body;
        if (!sessionId || !message) {
            return res.status(400).json({ error: 'Session ID and message are required.' });
        }

        await chats.insertOne({ sessionId, message, timestamp: new Date() });
        res.json({ message: 'Message saved successfully.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while saving the message.' });
    }
});

app.get('/get-history/:sessionId', async (req, res) => {
    try {
        const chats = await connectToDatabase();
        const sessionId = req.params.sessionId;
        if (!sessionId) {
            return res.status(400).json({ error: 'Session ID is required.' });
        }

        const chatHistory = await chats.find({ sessionId }).sort({ timestamp: 1 }).toArray();
        res.json({ history: chatHistory });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while retrieving chat history.' });
    }
});

const server = app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

const gracefulShutdown = () => {
    console.log('Initiating graceful shutdown...');
    if (dbClient) {
        dbClient.close().then(() => {
            console.log('Database connection closed.');
            server.close(() => {
                console.log('Server shut down.');
                process.exit();
            });
        }).catch(error => {
            console.error('Shutdown error:', error);
            process.exit(1);
        });
    } else {
        server.close(() => {
            console.log('Server shut down.');
            process.exit();
        });
    }
};

process.on('SIGINT', gracefulShutdown);
process.on('SIGTERM', gracefulShutdown);

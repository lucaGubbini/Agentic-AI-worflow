const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const port = 8001;
const mongoUri = 'mongodb://localhost:27017';

// Use Express built-in middleware for parsing JSON
app.use(express.json());

const client = new MongoClient(mongoUri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

async function connectToDatabase() {
    try {
        await client.connect();
        console.log('Connected successfully to database');
        return client.db('messaging').collection('messages');
    } catch (error) {
        console.error('Unable to connect to database:', error);
        process.exit(1); // Exit process with failure code
    }
}

app.post('/generate-code', async (req, res) => {
    const chats = await connectToDatabase();
    if (!chats) {
        return res.status(500).json({ error: 'Database connection not established.' });
    }

    try {
        const { description } = req.body;
        if (!description) {
            return res.status(400).json({ error: 'Description is required.' });
        }

        const generatedCode = `Code based on: ${description}`;
        await chats.insertOne({ prompt: description, response: generatedCode });
        res.status(200).json({ code: generatedCode });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred while generating code.' });
    }
});

async function startServer() {
    const server = app.listen(port, () => {
        console.log(`Server running on port ${port}`);
    });

    const gracefulShutdown = async () => {
        try {
            await client.close();
            console.log('Database connection closed.');
            server.close(() => {
                console.log('Server shut down.');
            });
        } catch (error) {
            console.error('Encountered error during shutdown:', error);
            process.exit(1);
        }
    };

    process.on('SIGINT', gracefulShutdown);
    process.on('SIGTERM', gracefulShutdown);
}

startServer();

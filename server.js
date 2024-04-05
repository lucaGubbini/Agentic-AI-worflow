const express = require('express');
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');

const app = express();
const port = 8001;
const mongoUri = 'mongodb://localhost:27017';

app.use(bodyParser.json());

const client = new MongoClient(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true });

async function main() {
    try {
        await client.connect();
        console.log('Connected successfully to database');

        const db = client.db('messaging');
        const chats = db.collection('messages');

        app.post('/generate-code', async (req, res) => {
            try {
                const { description } = req.body;
                const generatedCode = `Code based on: ${description}`;
                await chats.insertOne({ prompt: description, response: generatedCode });
                res.status(200).json({ code: generatedCode });
            } catch (error) {
                console.error(error);
                res.status(500).json({ error: 'An error occurred while generating code.' });
            }
        });

        const server = app.listen(port, () => {
            console.log(`Server running on port ${port}`);
        });

        const exitHandler = async () => {
            try {
                await client.close();
                console.log('Database connection closed.');
                server.close(() => {
                    console.log('Server shut down.');
                });
            } catch (e) {
                console.error('Encountered error during shutdown:', e);
                process.exit(1);
            }
        };

        process.on('SIGINT', exitHandler);
        process.on('SIGTERM', exitHandler);
    } catch (e) {
        console.error('Unable to connect to database:', e);
    }
}

main().catch(console.error);

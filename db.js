const { MongoClient } = require('mongodb');

const uri = process.env.MONGO_URI;
let dbClient = null;
let db = null;

async function connect() {
    if (!dbClient) {
        try {
            dbClient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
            await dbClient.connect();
            db = dbClient.db(process.env.DB_NAME);
            console.log('Successfully connected to database');
        } catch (error) {
            console.error('Database connection error:', error);
            process.exit(1); // Exit process if database connection fails
        }
    }
}

function getDb() {
    if (!db) {
        throw new Error('No database connection. Call connect first.');
    }
    return db;
}

async function close() {
    if (dbClient) {
        await dbClient.close();
        dbClient = null;
        db = null;
        console.log('Database connection closed');
    }
}

module.exports = { connect, getDb, close };

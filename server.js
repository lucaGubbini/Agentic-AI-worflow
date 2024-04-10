require('dotenv').config();
const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');
const helmet = require('helmet');
const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

// Modularizing route handlers
const chatRoutes = require('./routes/chatRoutes');
const agentRoutes = require('./routes/agentRoutes');
const db = require('./db');

const app = express();
const port = process.env.PORT || 8001;

// Middleware
app.use(cors({ origin: process.env.CORS_ORIGIN || '*' }));
app.use(helmet());
app.use(express.json());
app.use(express.static('public', { maxAge: '1d' })); // Cache static assets for 1 day for performance

// Use modularized route handlers
app.use('/chat', chatRoutes);
app.use('/agent', agentRoutes);

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Internal Server Error');
});

// SSL setup and server start
const startServer = async () => {
    await db.connect();

    if (process.env.USE_HTTPS === 'true') {
        const httpsOptions = {
            key: fs.readFileSync(path.resolve(process.env.SSL_KEY_PATH)),
            cert: fs.readFileSync(path.resolve(process.env.SSL_CERT_PATH)),
        };
        https.createServer(httpsOptions, app).listen(port, () => {
            console.log(`HTTPS server running at https://localhost:${port}`);
        });
    } else {
        http.createServer(app).listen(port, () => {
            console.log(`HTTP server running at http://localhost:${port}`);
        });
    }
};

startServer();

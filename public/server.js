require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

// Assuming db.js has been updated to not use deprecated options
const db = require('../db');

const app = express();
const port = process.env.PORT || 8001;

// Middleware
app.use(cors());
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            ...helmet.contentSecurityPolicy.getDefaultDirectives(),
            "script-src": ["'self'"],
            "style-src": ["'self'", "https://fonts.googleapis.com"],
            "font-src": ["'self'", "https://fonts.gstatic.com"],
        },
    },
}));
app.use(express.json());

// Static file serving
app.use(express.static(path.join(__dirname, 'public'), { maxAge: '1d' })); // Cache static assets

// Modularized route handlers
const chatRoutes = require('./routes/chatRoutes');
const agentRoutes = require('./routes/agentRoutes');
app.use('/chat', chatRoutes);
app.use('/agent', agentRoutes);

// Serve custom_agents.html directly
app.get('/custom-agents', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'custom_agents.html'));
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Internal Server Error');
});

// Database and server start
const startServer = async () => {
    try {
        await db.connect();
        console.log('Connected to database');
    } catch (err) {
        console.error('Failed to connect to database', err);
        process.exit(1);
    }

    // Server callback to log the server startup
    const serverCallback = () => {
        console.log(`Server running at http://localhost:${port}`);
    };

    // HTTPS setup if USE_HTTPS is true in the environment
    if (process.env.USE_HTTPS === 'true') {
        const httpsOptions = {
            key: fs.readFileSync(path.resolve(process.env.SSL_KEY_PATH)),
            cert: fs.readFileSync(path.resolve(process.env.SSL_CERT_PATH)),
        };
        https.createServer(httpsOptions, app).listen(port, serverCallback);
    } else {
        // HTTP server if not using HTTPS
        http.createServer(app).listen(port, serverCallback);
    }
};

startServer();

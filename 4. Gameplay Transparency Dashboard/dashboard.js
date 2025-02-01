const express = require('express');
const { createServer } = require('http');
const { WebSocketServer } = require('ws');
const crypto = require('crypto');
const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Blockchain Simulation
class GameIntegrityLedger {
    constructor() {
        this.chain = [];
        this.pendingVerifications = [];
    }

    createBlock(verificationData) {
        const block = {
            index: this.chain.length,
            timestamp: Date.now(),
            data: verificationData,
            previousHash: this.chain.length ? this.chain[this.chain.length - 1].hash : '0',
            nonce: 0
        };
        
        block.hash = this.calculateHash(block);
        this.chain.push(block);
        return block;
    }

    calculateHash(block) {
        return crypto
            .createHash('sha256')
            .update(
                block.index +
                block.timestamp +
                JSON.stringify(block.data) +
                block.previousHash +
                block.nonce
            )
            .digest('hex');
    }
}

// Initialize ledger
const ledger = new GameIntegrityLedger();

// Real-time WebSocket Updates
wss.on('connection', (ws) => {
    console.log('New client connected');
    
    ws.on('message', (message) => {
        const { type, gameId } = JSON.parse(message);
        if (type === 'subscribe') {
            // Send periodic updates
            const interval = setInterval(() => {
                const verificationData = generateVerificationPayload(gameId);
                ws.send(JSON.stringify(verificationData));
            }, 5000);

            ws.on('close', () => clearInterval(interval));
        }
    });
});

// Verification Engine
function generateVerificationPayload(gameId) {
    const gameData = getGameStatistics(gameId);
    const verificationHash = crypto
        .createHash('sha256')
        .update(JSON.stringify(gameData))
        .digest('hex');

    const block = ledger.createBlock({
        gameId,
        hash: verificationHash,
        timestamp: Date.now()
    });

    return {
        status: 'verified',
        blockIndex: block.index,
        verificationHash: block.hash,
        riskScore: calculateRiskScore(gameData),
        odds: gameData.odds
    };
}

// API Endpoints
app.get('/api/verify/:gameId', (req, res) => {
    const verification = generateVerificationPayload(req.params.gameId);
    res.json(verification);
});

app.get('/api/ledger', (req, res) => {
    res.json(ledger.chain);
});

server.listen(3000, () => {
    console.log('Game Integrity API running on port 3000');
});

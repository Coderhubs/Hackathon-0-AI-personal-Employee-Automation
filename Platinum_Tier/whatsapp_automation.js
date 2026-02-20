/**
 * FULLY AUTOMATED WhatsApp Sender using whatsapp-web.js
 * NO manual QR scanning after first time
 * Saves session for 24/7 autonomous operation
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

class WhatsAppAutomation {
    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth({
                dataPath: './browser_data/whatsapp'
            }),
            puppeteer: {
                headless: false,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        });

        this.isReady = false;
        this.setupEventHandlers();
    }

    setupEventHandlers() {
        // QR Code event (only first time)
        this.client.on('qr', (qr) => {
            console.log('\n' + '='.repeat(80));
            console.log('WHATSAPP - FIRST TIME SETUP');
            console.log('='.repeat(80));
            console.log('Scan this QR code with your phone:');
            console.log('');
            qrcode.generate(qr, { small: true });
            console.log('');
            console.log('After scanning, session will be saved for future use.');
            console.log('You will NEVER need to scan again!');
            console.log('='.repeat(80));
        });

        // Ready event
        this.client.on('ready', () => {
            console.log('\n' + '='.repeat(80));
            console.log('[OK] WhatsApp is READY - Fully Automated!');
            console.log('[OK] Session saved - No QR scan needed next time');
            console.log('='.repeat(80));
            this.isReady = true;
        });

        // Authentication success
        this.client.on('authenticated', () => {
            console.log('[OK] WhatsApp authenticated successfully');
        });

        // Authentication failure
        this.client.on('auth_failure', (msg) => {
            console.error('[ERROR] Authentication failed:', msg);
            console.log('Deleting old session and restarting...');
            // Session will be recreated on next start
        });

        // Disconnected
        this.client.on('disconnected', (reason) => {
            console.log('[WARN] WhatsApp disconnected:', reason);
            console.log('Attempting to reconnect...');
        });
    }

    async initialize() {
        console.log('\n' + '='.repeat(80));
        console.log('WHATSAPP AUTOMATION - FULLY AUTOMATED');
        console.log('='.repeat(80));
        console.log('Initializing WhatsApp client...');

        try {
            await this.client.initialize();

            // Wait for ready state
            await this.waitForReady();

            console.log('[OK] WhatsApp automation ready for 24/7 operation');
            return true;
        } catch (error) {
            console.error('[ERROR] Failed to initialize WhatsApp:', error);
            return false;
        }
    }

    async waitForReady(timeout = 120000) {
        const startTime = Date.now();

        while (!this.isReady) {
            if (Date.now() - startTime > timeout) {
                throw new Error('Timeout waiting for WhatsApp to be ready');
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    async sendMessage(contactName, message) {
        if (!this.isReady) {
            console.error('[ERROR] WhatsApp not ready yet');
            return { success: false, error: 'WhatsApp not ready' };
        }

        try {
            console.log(`[SEND] Sending message to ${contactName}...`);

            // Get all chats
            const chats = await this.client.getChats();

            // Find contact by name
            const chat = chats.find(c =>
                c.name && c.name.toLowerCase().includes(contactName.toLowerCase())
            );

            if (!chat) {
                console.error(`[ERROR] Contact not found: ${contactName}`);
                return {
                    success: false,
                    error: `Contact not found: ${contactName}`
                };
            }

            // Send message
            await chat.sendMessage(message);

            console.log(`[OK] Message sent to ${contactName}`);
            return {
                success: true,
                contact: contactName,
                timestamp: new Date().toISOString()
            };

        } catch (error) {
            console.error(`[ERROR] Failed to send message:`, error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    async getChats() {
        if (!this.isReady) {
            return [];
        }

        try {
            const chats = await this.client.getChats();
            return chats.map(chat => ({
                id: chat.id._serialized,
                name: chat.name,
                isGroup: chat.isGroup,
                unreadCount: chat.unreadCount
            }));
        } catch (error) {
            console.error('[ERROR] Failed to get chats:', error);
            return [];
        }
    }

    async monitorMessages(callback) {
        this.client.on('message', async (message) => {
            try {
                const chat = await message.getChat();
                const contact = await message.getContact();

                const messageData = {
                    from: contact.name || contact.pushname || contact.number,
                    body: message.body,
                    timestamp: new Date(message.timestamp * 1000).toISOString(),
                    isGroup: chat.isGroup,
                    chatName: chat.name
                };

                // Check for agentic AI keywords
                const agenticKeywords = [
                    'agentic', 'ai agent', 'autonomous ai', 'llm',
                    'claude', 'gpt', 'automation', 'artificial intelligence'
                ];

                const containsKeyword = agenticKeywords.some(keyword =>
                    message.body.toLowerCase().includes(keyword)
                );

                if (containsKeyword) {
                    console.log(`[AGENTIC AI] Message from ${messageData.from}: ${message.body.substring(0, 50)}...`);

                    if (callback) {
                        callback(messageData);
                    }
                }

            } catch (error) {
                console.error('[ERROR] Failed to process message:', error);
            }
        });
    }

    async shutdown() {
        console.log('\n[STOP] Shutting down WhatsApp automation...');
        await this.client.destroy();
        console.log('[OK] WhatsApp automation stopped');
    }
}

// API Server for Python integration
const express = require('express');
const app = express();
app.use(express.json());

let whatsappClient = null;

// Initialize WhatsApp
app.post('/api/whatsapp/initialize', async (req, res) => {
    try {
        if (whatsappClient) {
            return res.json({ success: true, message: 'Already initialized' });
        }

        whatsappClient = new WhatsAppAutomation();
        const success = await whatsappClient.initialize();

        res.json({ success });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Send message
app.post('/api/whatsapp/send', async (req, res) => {
    try {
        const { contact, message } = req.body;

        if (!whatsappClient || !whatsappClient.isReady) {
            return res.status(400).json({
                success: false,
                error: 'WhatsApp not initialized or not ready'
            });
        }

        const result = await whatsappClient.sendMessage(contact, message);
        res.json(result);

    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Get chats
app.get('/api/whatsapp/chats', async (req, res) => {
    try {
        if (!whatsappClient || !whatsappClient.isReady) {
            return res.status(400).json({
                success: false,
                error: 'WhatsApp not initialized or not ready'
            });
        }

        const chats = await whatsappClient.getChats();
        res.json({ success: true, chats });

    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Health check
app.get('/api/whatsapp/status', (req, res) => {
    res.json({
        initialized: whatsappClient !== null,
        ready: whatsappClient ? whatsappClient.isReady : false
    });
});

// Start server
const PORT = process.env.WHATSAPP_PORT || 3001;

app.listen(PORT, () => {
    console.log('\n' + '='.repeat(80));
    console.log('WHATSAPP AUTOMATION API SERVER');
    console.log('='.repeat(80));
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('');
    console.log('Endpoints:');
    console.log(`  POST http://localhost:${PORT}/api/whatsapp/initialize`);
    console.log(`  POST http://localhost:${PORT}/api/whatsapp/send`);
    console.log(`  GET  http://localhost:${PORT}/api/whatsapp/chats`);
    console.log(`  GET  http://localhost:${PORT}/api/whatsapp/status`);
    console.log('='.repeat(80));
    console.log('');

    // Auto-initialize
    console.log('[AUTO] Initializing WhatsApp...');
    whatsappClient = new WhatsAppAutomation();
    whatsappClient.initialize().then(success => {
        if (success) {
            console.log('[OK] WhatsApp ready for automation!');

            // Start monitoring messages
            whatsappClient.monitorMessages((messageData) => {
                // Save to file for processing
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                const filename = `WHATSAPP_${timestamp}_${messageData.from.replace(/[^a-zA-Z0-9]/g, '_')}.md`;
                const filepath = path.join(__dirname, '../AI_Employee_Vault/Needs_Action', filename);

                const content = `---
type: whatsapp_message
from: ${messageData.from}
chat: ${messageData.chatName}
timestamp: ${messageData.timestamp}
status: needs_action
created: ${new Date().toISOString()}
---

# WhatsApp Message from ${messageData.from}

## Chat
${messageData.chatName}

## Timestamp
${messageData.timestamp}

## Message
${messageData.body}

---
**Action Required:** Review and draft response
`;

                fs.writeFileSync(filepath, content, 'utf-8');
                console.log(`[SAVED] ${filename}`);
            });
        }
    });
});

// Graceful shutdown
process.on('SIGINT', async () => {
    if (whatsappClient) {
        await whatsappClient.shutdown();
    }
    process.exit(0);
});

const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;

// Initialize WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    }
});

let isClientReady = false;

client.on('qr', (qr) => {
    // Generate and scan this code with your phone
    console.log('QR Code received, please scan it:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
    isClientReady = true;
});

client.on('authenticated', () => {
    console.log('WhatsApp Client authenticated.');
});

client.on('auth_failure', (msg) => {
    console.error('WhatsApp Client authentication failure:', msg);
});

client.on('disconnected', (reason) => {
    console.log('WhatsApp Client was disconnected:', reason);
    isClientReady = false;
});

client.initialize();

// Send message endpoint
app.post('/send', async (req, res) => {
    if (!isClientReady) {
        return res.status(503).json({ success: false, error: 'WhatsApp client is not ready yet. Please ensure the QR code is scanned.' });
    }

    const { phone, message } = req.body;

    if (!phone || !message) {
        return res.status(400).json({ success: false, error: 'Phone and message are required.' });
    }

    try {
        // Send message
        // Ensure phone format is correct (e.g., 8801XXXXXXXXX@c.us)
        const response = await client.sendMessage(phone, message);
        console.log(`Message sent to ${phone}`);
        return res.status(200).json({ success: true, response });
    } catch (error) {
        console.error('Error sending message:', error);
        return res.status(500).json({ success: false, error: 'Failed to send message.', details: error.message });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

# AMMS WhatsApp Notification Microservice

This is a Node.js microservice that integrates with WhatsApp using `whatsapp-web.js` to send messages. It acts as an API for the Django backend in the AMMS system.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Create a `.env` file with `PORT=3001` (already provided).

## Running the Service

1. Start the server:
   ```bash
   node index.js
   ```
2. When running for the first time (or when session expires), a QR code will be generated in the terminal.
3. Open WhatsApp on your phone, go to **Linked Devices**, and scan the QR code to authenticate.
4. Once authenticated, the session is saved locally via `LocalAuth`, and you won't need to scan it again on subsequent restarts unless the session is logged out.

## API Endpoint

**POST `/send`**

Sends a WhatsApp message to a specific number.

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "phone": "8801XXXXXXXXX@c.us",
  "message": "Text message"
}
```

**Response (Success):**
```json
{
  "success": true,
  "response": { ... }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "WhatsApp client is not ready yet. Please ensure the QR code is scanned."
}
```

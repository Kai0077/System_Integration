12a Webhook System: Exposee and Integrator Roles

Overview

This project simulates a GitHub-like webhook system where two roles interact:
	•	Exposee: Hosts the system and exposes events to external consumers.
	•	Integrator: Consumes events by registering a webhook to receive data.

Each participant plays both roles and switches midway.

⸻

Exposee Instructions

Objective

Allow integrators to:
	•	Register and unregister webhooks
	•	Receive notifications for specific events
	•	Test webhook connectivity via a ping mechanism

Event Types (Example Theme: Payment Processing)
	•	payment_received
	•	payment_processed
	•	invoice_processing
	•	invoice_completed

⸻

Endpoints

POST /webhooks/register

Register a URL to receive specific event types.

Request:
```
{
  "url": "https://integrator-url.loca.lt/webhook-receiver",
  "event_types": ["payment_received", "invoice_completed"]
}
```
Response:
```
{
  "message": "Webhook registered for: payment_received, invoice_completed"
}
```

⸻

DELETE /webhooks/unregister

Unregister a webhook for a specific event.

Request:
```
{
  "url": "https://integrator-url.loca.lt/webhook-receiver",
  "event": "payment_received"
}
```
Response:
```
{
  "message": "1 webhook(s) unregistered"
}
```

⸻

GET /ping

Trigger a test event to all registered webhooks.

Sends:
```
{
  "event": "ping",
  "data": "Ping from Exposee"
}
```

⸻

POST /trigger

Trigger a specific event and send data to all registered webhooks.

Request:
```
{
  "event": "payment_received",
  "data": { "amount": 100, "currency": "USD" }
}
```

⸻

POST /webhooks/ping-back

Allows integrator to confirm receipt of a ping and get the original ping payload back.

Request:
```
{
  "url": "https://integrator-url.loca.lt/webhook-receiver"
}
```

⸻

Internals: Webhook Storage
	•	Webhooks are stored in a local file: webhooks.json
	•	Each entry includes a URL and an event name
	•	Supports multiple events per URL

⸻

Integrator Instructions

Objective
	•	Set up a local server to receive webhooks
	•	Create a script to register this server with the exposee

⸻

1. Webhook Receiver (app.js)
```
import express from 'express';
const app = express();
app.use(express.json());

app.post('/webhook-receiver', (req, res) => {
  console.log('Received webhook payload:', req.body);
  res.sendStatus(204);
});

app.listen(8080, () => {
  console.log('Listening on port 8080');
});
```
Use a tunneling tool (like LocalTunnel or Pinggy) to expose your server.
```
lt --port 8080 --subdomain example-integrator
```

⸻

2. Registration Script (registerWebhook.js)
```
import axios from 'axios';

const EXPOSEE_URL = 'https://example-exposee.loca.lt';
const WEBHOOK_URL = 'https://example-integrator.loca.lt/webhook-receiver';
const EVENT_TYPES = ['payment_received'];


```
```
async function registerWebhook() {
  try {
    const res = await axios.post(`${EXPOSEE_URL}/webhooks/register`, {
      url: WEBHOOK_URL,
      event_types: EVENT_TYPES
    });
    console.log('Register Response:', res.status, res.data);
  } catch (err) {
    console.error('Registration failed:', err.response?.data || err.message);
  }
}

registerWebhook();

```
⸻


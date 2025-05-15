# Webhook System

This server exposes a webhook service, allowing external applications to be notified when certain events happen.

## Overview of Operation

1. External applications (receivers) run a web server ready to accept incoming webhook notifications.
    
2. These applications register their public URL and choose which event types they want to receive via the webhook system's API.
    
3. When the webhook system processes an event, it automatically sends an HTTP POST with the event data to all registered subscribers.
    
## Supported Events

Subscribers can choose the receiving notifications for the following events:

- `payment_received`
    
- `payment_processed`
    
- `invoice_processing`
    
- `invoice_completed`
    

## Requirements for Receivers

To connect to this webhook system, a receiver must have:

- A web server actively running and able to handle HTTP POST requests.
    
- A way to interact with the API—this could be a script, CLI tool like `curl`, or API testing tool such as `Postman`.
    

Receiver servers should:

- Listen for incoming `POST` requests on a designated route.
    
- Parse JSON request bodies properly.
    
- Return a `200 OK` response to confirm that the webhook was successfully received.
    

### API Usage Guide

All requests should be directed to the base URL of the webhook system:

**Webhook Base URL:** `https://wide-apples-say.loca.lt`

#### 1. Register Your Webhook

Subscribe a receiver URL to one or more event types.

- **Endpoint:** `/register`
    
- **Method:** `POST`
    

**Request Example:**
```json
{
  "url": "WEBHOOK_RECEIVER_URL",
  "event": ["event2", "event3"]
}
```

- **Request URL:** `https://wide-apples-say.loca.lt/webhooks/register`
    

**Successful Response (`200 OK`):**
```json
{ 
  "message": "Webhook registered for: event" 
}
```

#### 2. Remove a Webhook

Unsubscribe a webhook from selected events or remove it entirely.

- **Endpoint:** `/unregister`
    
- **Method:** `DELETE`
    

**Request URL:** `https://nasty-ways-kneel.loca.lt/unregister`

**Request Body:**
```json
{
  "url": "REGISTERED_WEBHOOK_RECEIVER_URL",
  "event": ["event1"]
}
```

- If `event_types` is missing or an empty array, all events for that URL will be removed.
    
- If specified, only matching subscriptions for those event types will be removed.
    

**Success Response (`200 OK`):**
```json
{
  "message": "1 webhook(s) unregistered"
}
```
#### 3. Test Webhook with Ping

Send a test webhook to all registered subscribers to confirm connectivity.

- **Endpoint:** `/ping`
    
- **Method:** `GET`
    

**Request URL:** `https://nasty-ways-kneel.loca.lt/ping`

**Success Response (`200 OK`):**
```json
{ 
  "message": "Ping sent." 
}
```
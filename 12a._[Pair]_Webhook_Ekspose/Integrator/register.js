import axios from 'axios';

// Your friend's FastAPI server (Exposee)
const FRIEND_EXPOSEE_URL = 'https://eager-carpets-unite.loca.lt';

// Your public webhook receiver (Integrator)
const YOUR_WEBHOOK_URL = 'https://shaky-symbols-refuse.loca.lt/webhook-receiver';

// Must match allowed events (ask your friend or look in their code)
const EVENT = 'payment.received';

async function registerWebhook() {
  const payload = {
    url: YOUR_WEBHOOK_URL,
    event_types: [EVENT], 
  };

  try {
    const response = await axios.post(`${FRIEND_EXPOSEE_URL}/register`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 5000,
    });

    console.log(`✅ Register Response: ${response.status} —`, response.data);
  } catch (error) {
    const errorData = error.response?.data || error.message;
    console.error(`❌ Failed to register webhook:`, errorData);
  }
}

registerWebhook();
import axios from 'axios';

const WEBHOOK_BASE_URL = 'https://gentle-dancers-tie.loca.lt';

const RECEIVER_URL = 'https://blue-worms-heal.loca.lt/webhook-receiver';

const EVENT = 'payment.received';

async function registerWebhook() {
  const payload = {
    url: RECEIVER_URL,
    event_types: [EVENT], 
  };

  try {
    const response = await axios.post(`${WEBHOOK_BASE_URL}/register`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 5000,
    });

    console.log(`Register Response: ${response.status} —`, response.data);
  } catch (error) {
    const errorData = error.response?.data || error.message;
    console.error(`Failed to register webhook:`, errorData);
  }
}

registerWebhook();
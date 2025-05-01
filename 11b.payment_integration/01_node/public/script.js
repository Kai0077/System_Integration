const paypal_sdk_url = "https://www.paypal.com/sdk/js";
const client_id =  "AT8nhByn2hrfFGNrh0FI95obIxsXofEBt_n7OTC8NScC3jeaucv2a7_n7AfTZBXRV308rr695v6aOPZc";
const currency = "USD";
const intent = "capture";

function loadPaypalSdk() {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `${paypal_sdk_url}?client-id=${client_id}&currency=${currency}&intent=${intent}`;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

loadPaypalSdk()
  .then(() => {
    paypal.Buttons({
      style: { layout: 'vertical' },

      createOrder: () => {
        return fetch("/create_order", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ intent })
        })
        .then(res => res.json())
        .then(order => order.id);
      },

      onApprove: (data) => {
        return fetch("/complete_order", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ intent, order_id: data.orderID })
        })
        .then(res => res.json())
        .then(order => {
          const capture = order.purchase_units[0].payments[intent === "authorize" ? "authorizations" : "captures"][0];
          document.getElementById("alerts").innerText =
            `Thank you ${order.payer.name.given_name}! Payment of ${capture.amount.value} ${capture.amount.currency_code} received.`;
        });
      },

      onCancel: () => {
        document.getElementById("alerts").innerText = "Payment cancelled.";
      },

      onError: (err) => {
        console.error(err);
        document.getElementById("alerts").innerText = "Something went wrong.";
      }

    }).render('#paypal-button-container');
  })
  .catch(err => console.error("Failed to load PayPal SDK", err));
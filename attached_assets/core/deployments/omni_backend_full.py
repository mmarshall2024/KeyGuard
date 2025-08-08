
import stripe, os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
def handle_stripe_event(payload, sig_header):
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print("License delivered to", session.get("customer_email", "unknown"))
        return "", 200
    except Exception as e:
        return str(e), 400

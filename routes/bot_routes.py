from flask import Blueprint, request, jsonify
import stripe
import logging
from config import config

bot_bp = Blueprint('bot', __name__)
logger = logging.getLogger(__name__)

@bot_bp.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    """Handle Telegram webhook updates"""
    try:
        from app import app
        update_data = request.get_json(force=True)
        
        if hasattr(app, 'bot_core'):
            app.bot_core.process_telegram_update(update_data)
        
        return "OK"
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return "Error", 500

@bot_bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        
        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload, 
                sig_header, 
                config.get('STRIPE_WEBHOOK_SECRET', 'whsec_test')
            )
        except ValueError:
            return "Invalid payload", 400
        except stripe.error.SignatureVerificationError:
            return "Invalid signature", 400
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            logger.info(f"Payment succeeded: {payment_intent['id']}")
            
            # Store payment record or trigger actions
            # You can add custom logic here
            
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            logger.warning(f"Payment failed: {payment_intent['id']}")
            
        else:
            logger.info(f"Unhandled event type: {event['type']}")
        
        return "", 200
        
    except Exception as e:
        logger.error(f"Stripe webhook error: {e}")
        return "Error", 500

@bot_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session"""
    try:
        # Get domain for redirects
        domain = request.host_url.rstrip('/')
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'OMNICore Bot Premium Service',
                        'description': 'Access to premium bot features and services',
                    },
                    'unit_amount': 2000,  # $20.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payment/success',
            cancel_url=domain + '/payment/cancel',
            automatic_tax={'enabled': False},
        )
        
        return jsonify({'checkout_url': checkout_session.url})
        
    except Exception as e:
        logger.error(f"Stripe checkout error: {e}")
        return jsonify({'error': str(e)}), 500

@bot_bp.route('/payment/success')
def payment_success():
    """Payment success page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <div class="alert alert-success">
            <h1>✅ Payment Successful!</h1>
            <p>Thank you for your payment. Your OMNICore Bot premium features are now active.</p>
            <a href="/" class="btn btn-primary">Return to Home</a>
        </div>
    </body>
    </html>
    """

@bot_bp.route('/payment/cancel')
def payment_cancel():
    """Payment cancelled page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Cancelled</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <div class="alert alert-warning">
            <h1>⚠️ Payment Cancelled</h1>
            <p>Your payment was cancelled. No charges were made to your account.</p>
            <a href="/" class="btn btn-secondary">Return to Home</a>
        </div>
    </body>
    </html>
    """

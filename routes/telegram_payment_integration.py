from flask import Blueprint, request, jsonify, render_template
import os
import json
import logging
from datetime import datetime

telegram_payment_bp = Blueprint('telegram_payment', __name__)
logger = logging.getLogger(__name__)

# Telegram configuration
TELEGRAM_GROUP_CHAT_ID = "-1001987654321"
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

@telegram_payment_bp.route('/telegram-payment-link')
def telegram_payment_link():
    """Generate payment links for Telegram group"""
    return render_template('telegram_payment_integration.html', 
                         chat_id=TELEGRAM_GROUP_CHAT_ID)

@telegram_payment_bp.route('/send-payment-notification', methods=['POST'])
def send_payment_notification():
    """Send payment notifications to Telegram group"""
    try:
        data = request.get_json()
        amount = data.get('amount', 0)
        product_name = data.get('product_name', 'OMNI Empire Product')
        customer_name = data.get('customer_name', 'Customer')
        
        # Payment notification message
        message = f"""
🎉 **New Payment Received!**

💰 Amount: ${amount}
📦 Product: {product_name}
👤 Customer: {customer_name}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Revenue: ${get_total_revenue()}
        """
        
        # Send to Telegram group (requires bot token)
        if TELEGRAM_BOT_TOKEN:
            send_telegram_message(TELEGRAM_GROUP_CHAT_ID, message)
            return jsonify({'status': 'success', 'message': 'Notification sent to Telegram'})
        else:
            return jsonify({'status': 'warning', 'message': 'Telegram bot token not configured'})
            
    except Exception as e:
        logger.error(f"Telegram notification error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@telegram_payment_bp.route('/payment-commands')
def payment_commands():
    """Display Telegram bot payment commands"""
    commands = [
        {
            'command': '/payment_status',
            'description': 'Check current payment system status'
        },
        {
            'command': '/revenue_today',
            'description': 'Show today\'s revenue'
        },
        {
            'command': '/payment_methods',
            'description': 'List all available payment methods'
        },
        {
            'command': '/create_payment_link <amount> <product>',
            'description': 'Generate a payment link'
        },
        {
            'command': '/payment_analytics',
            'description': 'Show payment analytics'
        }
    ]
    
    return jsonify({
        'chat_id': TELEGRAM_GROUP_CHAT_ID,
        'commands': commands,
        'setup_instructions': 'Add the bot to your Telegram group and use these commands'
    })

def send_telegram_message(chat_id, message):
    """Send message to Telegram chat"""
    import requests
    
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not available")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {str(e)}")
        return False

def get_total_revenue():
    """Get total revenue from database"""
    try:
        from app import db
        from models_business import Transaction
        
        total = db.session.query(db.func.sum(Transaction.amount)).scalar()
        return f"{total:.2f}" if total else "0.00"
    except Exception:
        return "0.00"

@telegram_payment_bp.route('/webhook/payment-success', methods=['POST'])
def payment_success_webhook():
    """Webhook for successful payments to notify Telegram"""
    try:
        data = request.get_json()
        
        # Send notification to Telegram group
        send_payment_notification()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
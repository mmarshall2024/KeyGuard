from flask import Blueprint, render_template, request, jsonify
import json
from datetime import datetime

telegram_test_bp = Blueprint('telegram_test', __name__)

@telegram_test_bp.route('/telegram-test')
def telegram_test_interface():
    """Test interface for Telegram bot"""
    return render_template('telegram/test_interface.html')

@telegram_test_bp.route('/api/test-telegram-message', methods=['POST'])
def test_telegram_message():
    """Test telegram message processing without sending to real Telegram"""
    try:
        from flask import current_app
        data = request.get_json()
        
        message_text = data.get('message', '')
        user_name = data.get('user_name', 'TestUser')
        chat_id = data.get('chat_id', 123456789)
        
        # Create test update
        test_update = {
            "update_id": int(datetime.now().timestamp()),
            "message": {
                "message_id": int(datetime.now().timestamp()) % 1000,
                "from": {
                    "id": chat_id,
                    "first_name": user_name,
                    "username": user_name.lower()
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": message_text
            }
        }
        
        # Get bot core instance
        if hasattr(current_app, 'bot_core'):
            bot_core = current_app.bot_core
        else:
            from bot_core import BotCore
            bot_core = BotCore()
            bot_core.setup_bot()
            bot_core.load_plugins()
            current_app.bot_core = bot_core
        
        # Process the update and capture response
        original_send = bot_core.send_telegram_message
        captured_response = []
        
        def capture_message(chat_id, text):
            captured_response.append({
                'chat_id': chat_id,
                'text': text,
                'timestamp': datetime.now().isoformat()
            })
            return True
        
        # Replace send method temporarily
        bot_core.send_telegram_message = capture_message
        
        try:
            bot_core.process_telegram_update(test_update)
        finally:
            # Restore original method
            bot_core.send_telegram_message = original_send
        
        # Return the captured response
        if captured_response:
            return jsonify({
                'success': True,
                'message_sent': True,
                'response': captured_response[0]['text'],
                'processing_time': '< 0.1s',
                'bot_status': 'active'
            })
        else:
            return jsonify({
                'success': True,
                'message_sent': False,
                'response': 'No response generated',
                'processing_time': '< 0.1s',
                'bot_status': 'active'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'bot_status': 'error'
        }), 500

@telegram_test_bp.route('/api/telegram-bot-status')
def get_telegram_bot_status():
    """Get current Telegram bot status"""
    try:
        import os
        import requests
        
        token = os.environ.get('TELEGRAM_TOKEN')
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'No Telegram token configured'
            })
        
        # Check bot info
        bot_api_url = f"https://api.telegram.org/bot{token}/getMe"
        webhook_api_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
        
        bot_response = requests.get(bot_api_url, timeout=10)
        webhook_response = requests.get(webhook_api_url, timeout=10)
        
        bot_data = bot_response.json() if bot_response.status_code == 200 else {}
        webhook_data = webhook_response.json() if webhook_response.status_code == 200 else {}
        
        return jsonify({
            'status': 'active' if bot_data.get('ok') else 'error',
            'bot_info': bot_data.get('result', {}),
            'webhook_info': webhook_data.get('result', {}),
            'webhook_url': webhook_data.get('result', {}).get('url', 'Not set'),
            'pending_updates': webhook_data.get('result', {}).get('pending_update_count', 0),
            'last_error': webhook_data.get('result', {}).get('last_error_message', 'None'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
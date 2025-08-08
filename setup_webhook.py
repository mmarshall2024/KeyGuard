#!/usr/bin/env python3
"""
Script to set up Telegram webhook for OMNICore Bot
"""
import os
import requests

def setup_telegram_webhook():
    """Setup Telegram webhook"""
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        print("❌ No Telegram token found")
        return False
    
    # Get the webhook URL from Replit domain
    if os.environ.get('REPLIT_DEPLOYMENT') == '':
        # Development environment
        webhook_url = f"https://{os.environ.get('REPLIT_DEV_DOMAIN')}/telegram-webhook"
    else:
        # Production deployment
        domains = os.environ.get('REPLIT_DOMAINS', '').split(',')
        webhook_url = f"https://{domains[0]}/telegram-webhook" if domains else None
    
    if not webhook_url:
        print("❌ Could not determine webhook URL")
        return False
    
    # Set webhook
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {
        'url': webhook_url,
        'allowed_updates': ['message', 'callback_query']
    }
    
    print(f"🔗 Setting webhook to: {webhook_url}")
    
    try:
        response = requests.post(api_url, json=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook set successfully!")
            print(f"Description: {result.get('description', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting webhook: {e}")
        return False

def check_webhook_status():
    """Check current webhook status"""
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        print("❌ No Telegram token found")
        return
    
    api_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(api_url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            webhook_info = result['result']
            print("📊 Webhook Status:")
            print(f"  URL: {webhook_info.get('url', 'Not set')}")
            print(f"  Pending updates: {webhook_info.get('pending_update_count', 0)}")
            print(f"  Last error: {webhook_info.get('last_error_message', 'None')}")
            
            if webhook_info.get('url'):
                print("✅ Webhook is configured")
            else:
                print("⚠️ No webhook configured")
        else:
            print(f"❌ Failed to get webhook info: {result.get('description', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error checking webhook: {e}")

def get_bot_info():
    """Get bot information"""
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        print("❌ No Telegram token found")
        return
    
    api_url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(api_url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result['result']
            print("🤖 Bot Information:")
            print(f"  Name: {bot_info.get('first_name', 'N/A')}")
            print(f"  Username: @{bot_info.get('username', 'N/A')}")
            print(f"  ID: {bot_info.get('id', 'N/A')}")
            print(f"  Can join groups: {bot_info.get('can_join_groups', False)}")
            print(f"  Can read all group messages: {bot_info.get('can_read_all_group_messages', False)}")
        else:
            print(f"❌ Failed to get bot info: {result.get('description', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")

if __name__ == "__main__":
    print("🚀 OMNICore Bot Telegram Setup")
    print("=" * 40)
    
    # Check bot info
    get_bot_info()
    print()
    
    # Check current webhook status
    check_webhook_status()
    print()
    
    # Setup webhook
    if setup_telegram_webhook():
        print()
        print("🎉 Setup complete! Your bot is ready to receive messages.")
        print("💬 Try sending /start to your bot in Telegram!")
    else:
        print()
        print("❌ Setup failed. Please check your token and try again.")
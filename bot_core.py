import logging
import stripe
import requests
import json
from config import config
from plugin_manager import PluginManager

logger = logging.getLogger(__name__)

class BotCore:
    """Core bot functionality with dynamic command registration"""
    
    def __init__(self):
        self.telegram_token = config.telegram_token
        self.plugin_manager = PluginManager()
        
        # Initialize Stripe if key is available
        if config.stripe_secret_key:
            stripe.api_key = config.stripe_secret_key
        
        logger.info("Bot core initialized")
        
    def setup_bot(self):
        """Setup bot - simplified for web-only mode"""
        logger.info("Bot setup completed")
    
    def load_plugins(self):
        """Load and register plugin commands"""
        plugins = self.plugin_manager.load_all_plugins()
        logger.info(f"Loaded {len(plugins)} plugins")
    
    def process_telegram_update(self, update_data):
        """Process incoming Telegram update - simplified webhook handler"""
        try:
            # For now, just log the update
            logger.info(f"Received Telegram update: {json.dumps(update_data, indent=2)}")
            
            # Extract message info
            if 'message' in update_data:
                message = update_data['message']
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')
                
                # Simple command handling
                if text.startswith('/start'):
                    response = self.handle_start_command()
                elif text.startswith('/status'):
                    response = self.handle_status_command()
                elif text.startswith('/help'):
                    response = self.handle_help_command()
                else:
                    # Check plugin commands
                    response = self.handle_plugin_command(text, chat_id)
                    if not response:
                        response = "🤖 OMNICore Bot is active. Use /help for commands."
                
                # Send response back to Telegram
                if chat_id:
                    self.send_telegram_message(chat_id, response)
                    
        except Exception as e:
            logger.error(f"Error processing Telegram update: {e}")
    
    def handle_start_command(self):
        """Handle /start command"""
        return """🤖 OMNICore Bot Activated - Self-Evolving System

🧠 Core Features:
• Payment processing (Stripe)
• Auto-updates and plugins
• Multi-platform integration
• System monitoring

Type /help to explore all commands."""
    
    def handle_status_command(self):
        """Handle /status command"""
        status_parts = ["🔍 System Status:", "", "✅ Web Server: Online"]
        
        # Check Stripe
        try:
            if config.stripe_secret_key:
                stripe.Account.retrieve()
                status_parts.append("✅ Stripe: Connected")
            else:
                status_parts.append("⚠️ Stripe: No API key")
        except Exception:
            status_parts.append("❌ Stripe: Error")
        
        # Plugin status
        active_plugins = len(self.plugin_manager.get_active_plugins())
        status_parts.append(f"🔌 Active Plugins: {active_plugins}")
        
        return "\n".join(status_parts)
    
    def handle_help_command(self):
        """Handle /help command"""
        help_text = """🧠 OMNICore Commands:

/start - Activate the system
/help - Show this help
/status - System status check

**Plugin Commands:**
"""
        
        # Add plugin commands
        plugin_commands = self.plugin_manager.get_plugin_commands()
        if plugin_commands:
            for cmd, description in plugin_commands.items():
                help_text += f"/{cmd} - {description}\n"
        else:
            help_text += "No plugin commands available\n"
        
        help_text += "\n🌐 Admin Panel: Visit the web interface to manage plugins, updates, and configuration."
        return help_text
    
    def handle_plugin_command(self, text, chat_id):
        """Handle plugin commands"""
        try:
            # Extract command and args
            parts = text.split()
            if not parts or not parts[0].startswith('/'):
                return None
                
            command = parts[0][1:]  # Remove /
            args = parts[1:] if len(parts) > 1 else []
            
            # Check if this is a plugin command
            plugins = self.plugin_manager.get_active_plugins()
            for plugin_name, plugin_instance in self.plugin_manager.loaded_plugins.items():
                if hasattr(plugin_instance, 'commands') and command in plugin_instance.commands:
                    # Execute plugin command
                    if hasattr(plugin_instance, command):
                        handler = getattr(plugin_instance, command)
                        return handler(chat_id=chat_id, args=args)
                        
        except Exception as e:
            logger.error(f"Error handling plugin command: {e}")
            
        return None
    
    def send_telegram_message(self, chat_id, text):
        """Send message to Telegram"""
        try:
            if not self.telegram_token:
                logger.warning("No Telegram token available")
                return
                
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=data, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to send Telegram message: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")

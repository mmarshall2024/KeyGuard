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
                user_info = message.get('from', {})
                user_name = user_info.get('first_name', 'User')
                
                # Handle both commands and natural conversation
                if text.startswith('/start'):
                    response = self.handle_start_command()
                elif text.startswith('/status'):
                    response = self.handle_status_command()
                elif text.startswith('/help'):
                    response = self.handle_help_command()
                elif text.startswith('/'):
                    # Check plugin commands
                    response = self.handle_plugin_command(text, chat_id)
                    if not response:
                        response = f"I don't recognize that command. Type /help to see what I can do, or just chat with me naturally!"
                else:
                    # Track usage for AI suggestions
                    self.track_interaction(chat_id, text, user_name)
                    
                    # Handle natural conversation
                    response = self.handle_natural_chat(text, user_name, chat_id)
                
                # Send response back to Telegram
                if chat_id:
                    self.send_telegram_message(chat_id, response)
                    
        except Exception as e:
            logger.error(f"Error processing Telegram update: {e}")
    
    def handle_start_command(self):
        """Handle /start command"""
        return """🤖 OMNICore Bot Activated - Self-Evolving AI Assistant

Welcome! I'm not your typical bot - I love natural conversation! 

🗣️ **Just talk to me normally:**
• "Hello" or "Hi there!"
• "Tell me a joke"
• "What's the weather like in Paris?"
• "How are you doing?"
• "What can you help me with?"

🧠 **Core Features:**
• Natural conversation AI
• Weather information 
• Jokes and quotes
• Payment processing (Stripe)
• Auto-updates and plugins
• System monitoring

Try saying something like "Hello" or "What can you do?" - I prefer chatting over commands! 😊"""
    
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
        help_text = """🧠 OMNICore Bot - Your AI Assistant

**💬 Natural Chat:**
Just talk to me naturally! No need for commands:
• "Hello" - I'll greet you back
• "Tell me a joke" - I'll share something funny
• "Weather in London" - Get weather info
• "How are you?" - Chat about my status
• "What can you do?" - Learn my capabilities

**⚡ Quick Commands:**
/start - Activate the system
/help - Show this help  
/status - System status check

**🔌 Plugin Commands:**
"""
        
        # Add plugin commands
        plugin_commands = self.plugin_manager.get_plugin_commands()
        if plugin_commands:
            for cmd, description in plugin_commands.items():
                help_text += f"/{cmd} - {description}\n"
        else:
            help_text += "No plugin commands available\n"
        
        help_text += """\n💡 **Tip:** I prefer natural conversation! Instead of /joke, just say "tell me a joke" - it's more fun that way!

🌐 Admin Panel: Visit the web interface to manage plugins, updates, and configuration."""
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
    
    def handle_natural_chat(self, text, user_name, chat_id):
        """Handle natural conversation with the bot"""
        text_lower = text.lower()
        
        # Greetings
        if any(greeting in text_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            greetings = [
                f"Hello {user_name}! 👋 I'm your OMNICore bot assistant.",
                f"Hi there {user_name}! How can I help you today?",
                f"Hey {user_name}! Ready to explore what I can do?",
                f"Greetings {user_name}! I'm here to assist you."
            ]
            import random
            return random.choice(greetings) + "\n\nYou can ask me questions, request jokes, get weather updates, or just chat!"
        
        # Questions about capabilities
        elif any(phrase in text_lower for phrase in ['what can you do', 'what are you', 'capabilities', 'features']):
            return f"""I'm OMNICore, a self-evolving bot with many capabilities:

🤖 **Core Features:**
• Natural conversation (like we're doing now!)
• Payment processing with Stripe
• Weather information for any city
• Jokes and inspirational quotes
• System monitoring and updates
• Plugin architecture that grows over time

🗣️ **Chat with me naturally!** You can:
• Ask questions about anything
• Request "tell me a joke" or "weather in [city]"
• Say "how are you" or "what's new"
• Give me feedback or suggestions

Type /help for command list, or just keep chatting!"""
        
        # Weather requests in natural language
        elif 'weather' in text_lower:
            # Extract city from natural language
            words = text.split()
            city = None
            if 'in ' in text_lower:
                try:
                    in_index = words.index(next(word for word in words if word.lower().startswith('in')))
                    if in_index + 1 < len(words):
                        city = ' '.join(words[in_index + 1:])
                except:
                    pass
            
            if not city:
                return "I'd love to get weather for you! Which city would you like to know about?"
            
            # Use the weather plugin
            try:
                from plugin_manager import PluginManager
                pm = PluginManager()
                if 'example_plugin' in pm.loaded_plugins:
                    plugin = pm.loaded_plugins['example_plugin']
                    if hasattr(plugin, 'get_weather'):
                        return plugin.get_weather(chat_id=chat_id, args=[city])
            except:
                pass
            
            return f"Weather service is currently unavailable, but I'd check {city} for you if I could!"
        
        # Joke requests in natural language
        elif any(phrase in text_lower for phrase in ['joke', 'funny', 'make me laugh', 'humor']):
            try:
                from plugin_manager import PluginManager
                pm = PluginManager()
                if 'example_plugin' in pm.loaded_plugins:
                    plugin = pm.loaded_plugins['example_plugin']
                    if hasattr(plugin, 'get_joke'):
                        return plugin.get_joke(chat_id=chat_id)
            except:
                pass
            
            return "I'd tell you a joke, but my comedy plugin is taking a break! 😄"
        
        # Quote requests
        elif any(phrase in text_lower for phrase in ['quote', 'inspiration', 'motivate', 'inspire']):
            try:
                from plugin_manager import PluginManager
                pm = PluginManager()
                if 'example_plugin' in pm.loaded_plugins:
                    plugin = pm.loaded_plugins['example_plugin']
                    if hasattr(plugin, 'get_quote'):
                        return plugin.get_quote(chat_id=chat_id)
            except:
                pass
            
            return "Here's some inspiration: 'The best way to predict the future is to invent it!' - Alan Kay"
        
        # Questions about the bot's state
        elif any(phrase in text_lower for phrase in ['how are you', 'how do you feel', 'status']):
            return f"""I'm doing great, {user_name}! 🚀

My systems are:
✅ Online and responsive
✅ Learning from our conversations
✅ Ready to help with whatever you need

I love chatting naturally like this instead of just responding to commands. What would you like to talk about?"""
        
        # Payment/business inquiries
        elif any(phrase in text_lower for phrase in ['payment', 'buy', 'purchase', 'pay', 'cost', 'price']):
            return """I can help you with payments! 💳

I'm integrated with Stripe for secure payment processing. Whether you need to:
• Set up subscriptions
• Process one-time payments  
• Handle billing for services

Just let me know what you'd like to do, and I can create a secure checkout link for you!"""
        
        # Thanks/appreciation
        elif any(phrase in text_lower for phrase in ['thank', 'thanks', 'appreciate', 'great job']):
            responses = [
                f"You're very welcome, {user_name}! Happy to help! 😊",
                f"My pleasure, {user_name}! That's what I'm here for!",
                f"Glad I could help, {user_name}! Anything else you need?",
                f"Thanks {user_name}! I love being useful!"
            ]
            import random
            return random.choice(responses)
        
        # General conversation
        else:
            responses = [
                f"That's interesting, {user_name}! Tell me more about that.",
                f"I hear you, {user_name}. What would you like to explore together?",
                f"Thanks for sharing that! How can I help you today?",
                f"I'm here to chat and help however I can. What's on your mind?",
                f"Interesting! I love learning new things from our conversations.",
                f"I'm always ready to help or just have a friendly chat. What would you like to do?"
            ]
            import random
            return random.choice(responses) + "\n\nYou can ask me for jokes, weather, quotes, or just keep chatting!"
    
    def track_interaction(self, chat_id, text, user_name):
        """Track user interactions for AI analysis"""
        try:
            # Get AI suggestions plugin for usage tracking
            ai_plugin = self.plugin_manager.loaded_plugins.get('ai_suggestions_plugin')
            if ai_plugin and hasattr(ai_plugin, 'track_usage'):
                # Determine action type
                action = "natural_chat"
                if any(word in text.lower() for word in ['weather', 'forecast']):
                    action = "weather_request"
                elif any(word in text.lower() for word in ['joke', 'funny', 'laugh']):
                    action = "entertainment_request" 
                elif any(word in text.lower() for word in ['help', 'what can you do']):
                    action = "help_seeking"
                elif any(word in text.lower() for word in ['payment', 'pay', 'crypto', 'bitcoin']):
                    action = "payment_inquiry"
                
                context = {
                    "message_length": len(text),
                    "user_name": user_name,
                    "contains_question": "?" in text
                }
                
                ai_plugin.track_usage(chat_id, action, context)
        except Exception as e:
            logger.error(f"Error tracking interaction: {e}")
    
    def send_telegram_message(self, chat_id, text):
        """Send message to Telegram"""
        try:
            if not self.telegram_token:
                logger.warning("No Telegram token available")
                return False
                
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            # Handle long messages by splitting them
            max_length = 4096
            if len(text) > max_length:
                # Split into chunks
                chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
                success = True
                for chunk in chunks:
                    if not self._send_message_chunk(url, chat_id, chunk):
                        success = False
                return success
            else:
                return self._send_message_chunk(url, chat_id, text)
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def _send_message_chunk(self, url, chat_id, text):
        """Send a single message chunk to Telegram"""
        try:
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=data, timeout=15)
            
            if response.status_code == 200:
                logger.info(f"Message sent successfully to chat {chat_id}")
                return True
            else:
                logger.error(f"Failed to send message: {response.status_code} - {response.text}")
                # Try without markdown if it failed due to formatting
                if 'parse_mode' in data:
                    del data['parse_mode']
                    retry_response = requests.post(url, json=data, timeout=15)
                    if retry_response.status_code == 200:
                        logger.info(f"Message sent successfully without markdown to chat {chat_id}")
                        return True
                return False
                
        except Exception as e:
            logger.error(f"Error sending message chunk: {e}")
            return False

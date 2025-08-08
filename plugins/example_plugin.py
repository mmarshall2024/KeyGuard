from plugins.base_plugin import BasePlugin
import requests
import random

class ExamplePlugin(BasePlugin):
    """Example plugin demonstrating the plugin system"""
    
    def __init__(self):
        super().__init__()
        self.version = "1.0.1"
        self.description = "Example plugin with various commands"
    
    def register_commands(self, application=None):
        """Register plugin commands"""
        self.add_command("joke", self.get_joke, "Get a random joke")
        self.add_command("quote", self.get_quote, "Get an inspirational quote")
        self.add_command("weather", self.get_weather, "Get weather information")
        
        self.log(f"{self.name} commands registered successfully")
    
    def get_joke(self, chat_id=None, args=None):
        """Get a random joke"""
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
            if response.status_code == 200:
                joke_data = response.json()
                joke = f"{joke_data['setup']}\n\n{joke_data['punchline']}"
                return f"😂 **Random Joke:**\n\n{joke}"
            else:
                return "🤷 Sorry, couldn't fetch a joke right now!"
        except Exception as e:
            self.log(f"Joke API error: {e}", "error")
            # Fallback jokes
            fallback_jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the bot go to therapy? It had too many bugs!",
                "How do you comfort a JavaScript bug? You console it!"
            ]
            joke = random.choice(fallback_jokes)
            return f"😂 **Fallback Joke:**\n\n{joke}"
    
    def get_quote(self, chat_id=None, args=None):
        """Get an inspirational quote"""
        try:
            response = requests.get("https://api.quotable.io/random", timeout=5)
            if response.status_code == 200:
                quote_data = response.json()
                quote = f'"{quote_data["content"]}"\n\n— {quote_data["author"]}'
                return f"✨ **Inspirational Quote:**\n\n{quote}"
            else:
                return "🤷 Sorry, couldn't fetch a quote right now!"
        except Exception as e:
            self.log(f"Quote API error: {e}", "error")
            # Fallback quotes
            fallback_quotes = [
                '"The only way to do great work is to love what you do." — Steve Jobs',
                '"Innovation distinguishes between a leader and a follower." — Steve Jobs',
                '"The future belongs to those who believe in the beauty of their dreams." — Eleanor Roosevelt'
            ]
            quote = random.choice(fallback_quotes)
            return f"✨ **Inspirational Quote:**\n\n{quote}"
    
    def get_weather(self, chat_id=None, args=None):
        """Get weather information"""
        # Get location from command arguments
        location = " ".join(args) if args else "New York"
        
        try:
            # Using a free weather API (you can get API key from openweathermap.org)
            api_key = self.get_config("WEATHER_API_KEY", "demo_key")
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                weather_data = response.json()
                temp = weather_data['main']['temp']
                description = weather_data['weather'][0]['description'].title()
                city = weather_data['name']
                country = weather_data['sys']['country']
                
                weather_msg = f"🌤️ **Weather in {city}, {country}:**\n\n"
                weather_msg += f"🌡️ Temperature: {temp}°C\n"
                weather_msg += f"📝 Conditions: {description}\n"
                weather_msg += f"💨 Humidity: {weather_data['main']['humidity']}%"
                
                return weather_msg
            else:
                return f"🤷 Sorry, couldn't get weather for '{location}'"
        except Exception as e:
            self.log(f"Weather API error: {e}", "error")
            return (
                f"☁️ Weather service temporarily unavailable.\n\n"
                f"Usage: `/weather [city name]`\n"
                f"Example: `/weather London`"
            )

from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for all OMNICore plugins"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "Base plugin class"
        self.commands = {}
    
    @abstractmethod
    def register_commands(self, application=None):
        """Register plugin commands with the bot application"""
        pass
    
    def add_command(self, command_name, handler_func, description="No description"):
        """Helper method to add commands"""
        self.commands[command_name] = description
        return {'command': command_name, 'handler': handler_func, 'description': description}
    
    def get_config(self, key, default=None):
        """Get plugin-specific configuration"""
        from config import config
        return config.get(f"{self.name.upper()}_{key}", default)
    
    def log(self, message, level="info"):
        """Plugin logging helper"""
        import logging
        logger = logging.getLogger(f"plugin.{self.name}")
        getattr(logger, level)(message)

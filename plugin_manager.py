import os
import importlib
import importlib.util
import logging
from pathlib import Path
from models import Plugin
from app import db

logger = logging.getLogger(__name__)

class PluginManager:
    """Manage dynamic plugin loading and registration"""
    
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.loaded_plugins = {}
        self.plugin_commands = {}
    
    def load_all_plugins(self):
        """Load all enabled plugins from database and filesystem"""
        plugins = []
        
        # Get enabled plugins from database
        try:
            enabled_plugins = Plugin.query.filter_by(enabled=True).all()
            
            for plugin_record in enabled_plugins:
                try:
                    plugin = self.load_plugin(plugin_record.module_path)
                    if plugin:
                        plugins.append(plugin)
                        self.loaded_plugins[plugin_record.name] = plugin
                        # Register commands
                        if hasattr(plugin, 'register_commands'):
                            plugin.register_commands()
                        logger.info(f"Loaded plugin: {plugin_record.name}")
                        
                        # Auto-enable AI suggestions plugin
                        if plugin_record.name == 'ai_suggestions_plugin':
                            logger.info("AI Suggestions plugin loaded - usage tracking enabled")
                except Exception as e:
                    logger.error(f"Failed to load plugin {plugin_record.name}: {e}")
                    
        except Exception as e:
            logger.error(f"Database error loading plugins: {e}")
            
        # Auto-discover new plugins in filesystem
        self.discover_new_plugins()
        
        return plugins
    
    def load_plugin(self, module_path):
        """Load a specific plugin module"""
        try:
            if module_path.endswith('.py'):
                module_path = module_path[:-3]
            
            # Convert file path to module path
            module_name = module_path.replace('/', '.').replace('\\', '.')
            
            # Import the module
            if module_name in self.loaded_plugins:
                # Reload existing module
                importlib.reload(self.loaded_plugins[module_name])
            
            spec = importlib.util.spec_from_file_location(module_name, f"{module_path}.py")
            if not spec or not spec.loader:
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for plugin class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (hasattr(attr, '__bases__') and 
                    any('BasePlugin' in str(base) for base in attr.__bases__)):
                    return attr()
                    
            return None
            
        except Exception as e:
            logger.error(f"Error loading plugin from {module_path}: {e}")
            return None
    
    def discover_new_plugins(self):
        """Discover and register new plugins from filesystem"""
        if not self.plugin_dir.exists():
            return
            
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            plugin_name = plugin_file.stem
            module_path = str(plugin_file.relative_to("."))
            
            # Check if plugin is already registered
            existing = Plugin.query.filter_by(name=plugin_name).first()
            if existing:
                continue
                
            try:
                # Try to load and inspect the plugin
                plugin_instance = self.load_plugin(module_path[:-3])  # Remove .py
                if plugin_instance:
                    # Register new plugin in database
                    plugin_record = Plugin(
                        name=plugin_name,
                        version=getattr(plugin_instance, 'version', '1.0.0'),
                        module_path=module_path,
                        enabled=True
                    )
                    db.session.add(plugin_record)
                    db.session.commit()
                    
                    self.loaded_plugins[plugin_name] = plugin_instance
                    logger.info(f"Auto-registered new plugin: {plugin_name}")
                    
            except Exception as e:
                logger.error(f"Error auto-registering plugin {plugin_name}: {e}")
    
    def reload_plugin(self, plugin_name):
        """Hot-reload a specific plugin"""
        try:
            plugin_record = Plugin.query.filter_by(name=plugin_name).first()
            if not plugin_record:
                return False
                
            # Reload the plugin
            plugin_instance = self.load_plugin(plugin_record.module_path[:-3])
            if plugin_instance:
                self.loaded_plugins[plugin_name] = plugin_instance
                logger.info(f"Reloaded plugin: {plugin_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error reloading plugin {plugin_name}: {e}")
        
        return False
    
    def enable_plugin(self, plugin_name):
        """Enable a plugin"""
        try:
            plugin_record = Plugin.query.filter_by(name=plugin_name).first()
            if plugin_record:
                plugin_record.enabled = True
                db.session.commit()
                
                # Load the plugin
                plugin_instance = self.load_plugin(plugin_record.module_path[:-3])
                if plugin_instance:
                    self.loaded_plugins[plugin_name] = plugin_instance
                    return True
        except Exception as e:
            logger.error(f"Error enabling plugin {plugin_name}: {e}")
        
        return False
    
    def disable_plugin(self, plugin_name):
        """Disable a plugin"""
        try:
            plugin_record = Plugin.query.filter_by(name=plugin_name).first()
            if plugin_record:
                plugin_record.enabled = False
                db.session.commit()
                
                # Remove from loaded plugins
                if plugin_name in self.loaded_plugins:
                    del self.loaded_plugins[plugin_name]
                    
                return True
        except Exception as e:
            logger.error(f"Error disabling plugin {plugin_name}: {e}")
        
        return False
    
    def get_active_plugins(self):
        """Get dictionary of active plugins with their info"""
        active = {}
        for name, plugin in self.loaded_plugins.items():
            active[name] = {
                'version': getattr(plugin, 'version', 'unknown'),
                'description': getattr(plugin, 'description', 'No description'),
                'commands': getattr(plugin, 'commands', [])
            }
        return active
    
    def get_plugin_commands(self):
        """Get all commands provided by plugins"""
        commands = {}
        for plugin in self.loaded_plugins.values():
            if hasattr(plugin, 'commands'):
                commands.update(plugin.commands)
        return commands

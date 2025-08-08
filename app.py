import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///omnicore.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import routes and models after app creation
from routes.admin import admin_bp
from routes.bot_routes import bot_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(bot_bp)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Initialize bot core
    from bot_core import BotCore
    bot_core = BotCore()
    bot_core.setup_bot()
    bot_core.load_plugins()
    app.bot_core = bot_core
    
    logger.info("OMNICore Bot initialized successfully")

@app.route('/')
def index():
    return "🧠 OMNICore_Bot: LIVE - Self-Evolving System Active"

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    from utils.health_monitor import HealthMonitor
    monitor = HealthMonitor()
    status = monitor.get_system_status()
    return status, 200 if status['healthy'] else 503

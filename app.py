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
from routes.revenue_landing import revenue_landing_bp
from routes.analytics import analytics_bp
from routes.revenue import revenue_bp
from routes.landing_pages import landing_pages_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(bot_bp)
app.register_blueprint(revenue_landing_bp)
app.register_blueprint(analytics_bp, url_prefix='/analytics')
app.register_blueprint(revenue_bp)
# Register payment systems blueprint
from routes.payment_systems import payment_systems_bp
app.register_blueprint(payment_systems_bp)

# Register automation blueprint
from routes.automation_routes import automation_bp
app.register_blueprint(automation_bp)

# Register content AI blueprint
from routes.content_ai_routes import content_ai_bp
app.register_blueprint(content_ai_bp)

# Register main navigation blueprint
from routes.main_navigation import main_nav_bp
app.register_blueprint(main_nav_bp)

# Register payment earnings blueprint
from routes.payment_earnings_routes import payment_earnings_bp
app.register_blueprint(payment_earnings_bp)

with app.app_context():
    # Import models to ensure tables are created
    import models
    import models_business
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
    from flask import redirect, url_for
    return redirect('/empire')

@app.route('/empire-dashboard')
def empire_dashboard():
    """Complete empire overview dashboard"""
    return render_template('empire_dashboard.html')

@app.route('/payments')
def payments_redirect():
    """Redirect to payment systems dashboard"""
    from flask import redirect
    return redirect('/payment-dashboard')

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    from utils.health_monitor import HealthMonitor
    monitor = HealthMonitor()
    status = monitor.get_system_status()
    return status, 200 if status['healthy'] else 503

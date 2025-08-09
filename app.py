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

# Register Telegram payment integration blueprint
from routes.telegram_payment_integration import telegram_payment_bp
app.register_blueprint(telegram_payment_bp)

# Register empire master dashboard blueprint
from routes.empire_master_dashboard import empire_master_bp
app.register_blueprint(empire_master_bp)

# Register affiliate bot system blueprint
from routes.affiliate_bot_system import affiliate_bot_bp
app.register_blueprint(affiliate_bot_bp)

# Register setup checklist blueprint
from routes.setup_checklist_bot import setup_checklist_bp
app.register_blueprint(setup_checklist_bp)

# Register product catalog blueprint
from routes.product_catalog import product_catalog_bp
app.register_blueprint(product_catalog_bp)

# Register empire audit bot blueprint
from routes.empire_audit_bot import empire_audit_bp
app.register_blueprint(empire_audit_bp)

# Register campaign launcher blueprint
from routes.campaign_launcher import campaign_launcher_bp
app.register_blueprint(campaign_launcher_bp)

# Register chat support blueprint
from routes.chat_support import chat_support_bp
app.register_blueprint(chat_support_bp)

# Register campaign performance dashboard blueprint
from routes.campaign_performance_dashboard import campaign_performance_bp
app.register_blueprint(campaign_performance_bp)

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

# Register empire management blueprint
from routes.empire_routes import empire_bp
app.register_blueprint(empire_bp)

# Auto-start campaign launcher if needed

# Register campaign automation blueprint
from routes.campaign_automation import campaign_automation_bp
app.register_blueprint(campaign_automation_bp)

# Register instant money blueprint
from routes.instant_money import instant_money
app.register_blueprint(instant_money, url_prefix='/money')

with app.app_context():
    # Import models to ensure tables are created
    import models
    import models_business
    db.create_all()
    
    # Initialize bot core
    try:
        from bot_core import BotCore
        bot_core = BotCore()
        bot_core.setup_bot()
        bot_core.load_plugins()
        setattr(app, 'bot_core', bot_core)
    except Exception as e:
        logger.warning(f"Bot initialization warning: {str(e)}")
    
    logger.info("OMNICore Bot initialized successfully")

@app.route('/')
def index():
    from flask import render_template
    return render_template('empire_website_info.html')

@app.route('/dashboard')
def dashboard():
    from flask import render_template
    return render_template('empire_master_dashboard.html')

# Auto-start audit monitoring on app startup
def initialize_audit_monitoring():
    try:
        from routes.empire_audit_bot import audit_bot
        audit_bot.start_monitoring()
        logger.info("Auto-started Empire Audit Bot monitoring")
    except Exception as e:
        logger.warning(f"Could not auto-start audit monitoring: {str(e)}")

# Initialize audit monitoring after app setup
initialize_audit_monitoring()

# Initialize mutation evolution engine
def initialize_mutation_evolution():
    try:
        from utils.mutation_evolution import mutation_engine
        speech_activation = mutation_engine.activate_speech_synthesis()
        logger.info(f"Mutation evolution engine initialized - Speech synthesis: {speech_activation['status']}")
    except Exception as e:
        logger.warning(f"Could not initialize mutation evolution: {str(e)}")

initialize_mutation_evolution()

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

from app import app
from routes.landing_pages import landing_pages_bp
from routes.analytics import analytics_bp
from routes.deployment import deployment_bp
from routes.telegram_test import telegram_test_bp
from routes.revenue import revenue_bp
from flask import redirect

# Register blueprints
app.register_blueprint(landing_pages_bp, url_prefix='/landing')
app.register_blueprint(analytics_bp, url_prefix='/')
app.register_blueprint(deployment_bp, url_prefix='/')
app.register_blueprint(telegram_test_bp, url_prefix='/')
app.register_blueprint(revenue_bp, url_prefix='/')

# Add root redirect to revenue dashboard
@app.route('/')
def root_redirect():
    return redirect('/revenue')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

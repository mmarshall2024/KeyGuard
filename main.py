from app import app
from routes.landing_pages import landing_pages_bp

# Register landing pages blueprint
app.register_blueprint(landing_pages_bp, url_prefix='/landing')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

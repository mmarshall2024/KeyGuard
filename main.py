from app import app
from routes.landing_pages import landing_pages_bp
from flask import redirect

# Register landing pages blueprint
app.register_blueprint(landing_pages_bp, url_prefix='/landing')

# Add root redirect to landing page
@app.route('/')
def root_redirect():
    return redirect('/landing/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

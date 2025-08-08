
from flask import Flask, request, render_template, send_file, jsonify
import os
from omni_backend_full import handle_stripe_event, omni_logic_core
from license_vault import check_license
from recovery_engine import auto_heal
from observer_seed import observe_system
from mutation_engine import mutate_logic
from security_layer import sentinel_scan

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "omni_super_secure")

@app.route("/")
def dashboard():
    sentinel_scan()
    return render_template("index.html")

@app.route("/gpt-agent", methods=["POST"])
def run_agent():
    prompt = request.json.get("prompt")
    response = omni_logic_core(prompt)
    return jsonify({"response": response})

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    return handle_stripe_event(payload, sig_header)

@app.route("/download/<filename>")
def download(filename):
    if not check_license(request):
        return "Unauthorized", 403
    return send_file(f"drops/{filename}", as_attachment=True)

@app.route("/observer")
def observer():
    return jsonify(observe_system())

@app.route("/mutate")
def mutate():
    mutate_logic()
    return "Mutation Triggered", 200

if __name__ == "__main__":
    auto_heal()
    app.run(host="0.0.0.0", port=8080)

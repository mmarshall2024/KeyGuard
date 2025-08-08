
from flask import Flask, request
import requests, os
from gpt_core import omni_logic_core

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text.startswith("/ask"):
        prompt = text[5:].strip()
        reply = omni_logic_core(prompt)
    elif text == "/buy":
        reply = "🛒 Buy now: https://your-stripe-checkout-link"
    elif text == "/start":
        reply = "Welcome to OMNI AI."
    elif text == "/status":
        reply = "🧠 OMNI STATUS: Online, Mutating, Generating Revenue."
    else:
        reply = "Unknown command. Try /ask, /buy, /status"

    requests.post(f"{BOT_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })
    return "", 200

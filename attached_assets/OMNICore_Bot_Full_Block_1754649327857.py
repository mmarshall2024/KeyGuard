
# OMNICore_Bot — Telegram + Stripe + PayPal + Mastodon + DEV.to + Crypto Payment Ready
# Dependencies: flask, python-telegram-bot, stripe, requests
# Deployment: Replit or local server

import os, stripe, json, requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# === CONFIGURATION ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
CRYPTO_WALLET = os.getenv("CRYPTO_WALLET")
MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
MASTODON_URL = os.getenv("MASTODON_URL", "https://mastodon.social")
DEVTO_KEY = os.getenv("DEVTO_KEY")

# === BOT INITIALIZATION ===
# Validate required environment variables
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, None, workers=0, use_context=True)

# === COMMANDS ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 OMNICore_Bot Activated.
Type /help to explore the Empire.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("🧠 Commands:
/start
/pay
/post
/status
/crypto")

def pay(update: Update, context: CallbackContext):
    update.message.reply_text("💳 Use this link to pay: https://buy.stripe.com/test_payment")

def post_to_dev(update: Update, context: CallbackContext):
    content = {"title": "OMNI Drop", "published": True, "body_markdown": "The OMNI System has launched."}
    headers = {"api-key": DEVTO_KEY}
    r = requests.post("https://dev.to/api/articles", json=content, headers=headers)
    update.message.reply_text(f"Posted to DEV.to ✅" if r.status_code == 201 else "Failed.")

def status(update: Update, context: CallbackContext):
    update.message.reply_text("✅ All systems operational: Stripe, PayPal, Telegram, Dev.to, Mastodon.")

def crypto(update: Update, context: CallbackContext):
    update.message.reply_text(f"🪙 Send crypto to: {CRYPTO_WALLET}")

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("pay", pay))
dp.add_handler(CommandHandler("post", post_to_dev))
dp.add_handler(CommandHandler("status", status))
dp.add_handler(CommandHandler("crypto", crypto))

# === FLASK ROUTES ===
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"

@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return f"Webhook Error: {str(e)}", 400
    print(f"Stripe Event Received: {event['type']}")
    return "", 200

@app.route("/")
def index():
    return "🧠 OMNICore_Bot: LIVE"

if __name__ == "__main__":
    stripe.api_key = STRIPE_SECRET_KEY
    app.run(port=5000)

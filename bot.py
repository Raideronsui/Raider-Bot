import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Load token from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # DO NOT hardcode token here

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Raider Bot is live!")

# Bot command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start or /help")

# Build application
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Webhook route for Telegram
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Healthcheck
@app.route('/')
def index():
    return "Bot is running."

# Start Flask app
if __name__ == "__main__":
    app.run(port=10000)


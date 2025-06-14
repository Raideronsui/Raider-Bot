import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Raider Bot is live!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start or /help")

# Application
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route('/')
def home():
    return "Raider Bot is running."

if __name__ == "__main__":
    app.run(port=10000)


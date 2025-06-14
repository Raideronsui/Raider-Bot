from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7586933538:AAEdrgOLMGkKzpA94558_1uLj25rxb7NKds"  # Replace in dev if needed

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Raider Bot is live!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start or /help")

# Register commands
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Health check endpoint
@app.route("/", methods=["GET"])
def index():
    return "Bot is running."

# Local testing
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: application.run_polling()).start()
    app.run(host="0.0.0.0", port=10000)


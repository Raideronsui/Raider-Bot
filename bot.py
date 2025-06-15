import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set your bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask app
app = Flask(__name__)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# PTB Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Raider Bot is live!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start or /help")

# Add handlers to app
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Webhook route
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return 'ok', 200

# Health check
@app.route('/')
def index():
    return 'Raider Bot is running.'

# Start Flask app
if __name__ == '__main__':
    import asyncio
    # Start PTB (no polling — webhook only)
    asyncio.get_event_loop().create_task(application.initialize())
    app.run(host='0.0.0.0', port=10000)


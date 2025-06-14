from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

# Load token from environment (fallback to hardcoded if needed for local testing)
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7586933538:AAEdrgOLMGkKzpA94558_1uLj25rxb7NKds"

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0)

# Commands
def start(update, context):
    update.message.reply_text("Raider Bot is live!")

def help_command(update, context):
    update.message.reply_text("Use /start or /help")

# Register command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

# Webhook endpoint
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# Health check route
@app.route('/')
def index():
    return 'Raider Bot is up.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

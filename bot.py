from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

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

# Keep alive (for health check)
@app.route('/')
def index():
    return 'Bot is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

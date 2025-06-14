import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://github.com/Raideronsui/Raider-Bot/7586933538:AAEdrgOLMGkKzpA94558_1uLj25rxb7NKds"  # Replace with your Render URL

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Raider Bot is live!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start or /help")

# Register command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Flask route to receive updates
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Health check route
@app.route('/')
def index():
    return "Raider Bot is running."

if __name__ == "__main__":
    import asyncio
    asyncio.run(application.initialize())
    asyncio.run(application.bot.set_webhook(url=WEBHOOK_URL))
    app.run(host="0.0.0.0", port=10000)

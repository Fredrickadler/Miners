from flask import Flask, render_template, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging

TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"
URL = "https://miners-1.onrender.com"

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming updates from Telegram."""
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update: Update, context):
    update.message.reply_text("Welcome to the Miner Bot!")

def echo(update: Update, context):
    update.message.reply_text(f"You said: {update.message.text}")

def error(update: Update, context):
    logger.warning(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    # Telegram Dispatcher setup
    dispatcher = Dispatcher(bot, None, workers=0)

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error)

    # Set webhook
    bot.set_webhook(f"{URL}/{TOKEN}")

    # Run Flask server
    app.run(host="0.0.0.0", port=5000)
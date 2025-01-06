دریافت پیام‌های وب‌ه from flask import Flask, render_template, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Dispatcher

# Telegram Bot Token
TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Flask route for the web interface
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle Telegram webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Command handler for /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Miner Bot!")

# Initialize dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    # Set webhook
    bot.set_webhook(url=f"https://your-server-url.com/{TOKEN}")
    # Run Flask app
    app.run(host="0.0.0.0", port=5000)
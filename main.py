
from flask import Flask, render_template
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater

TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Miner Bot!")

if __name__ == "__main__":
    # Run Flask for the web interface
    app.run(host="0.0.0.0", port=5000)

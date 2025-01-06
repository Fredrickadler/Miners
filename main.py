from flask import Flask, render_template, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater

# توکن بات تلگرام
TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"

# آدرس سرور
SERVER_URL = "https://miners-1.onrender.com"

# ایجاد اپلیکیشن Flask
app = Flask(__name__)

# مسیری برای صفحه وب ماینر
@app.route("/")
def index():
    return render_template("index.html")

# تابع شروع برای بات تلگرام
def start(update: Update, context: CallbackContext):
    # ایجاد دکمه "Open" با لینک به صفحه وب
    keyboard = [[InlineKeyboardButton("Open", url=SERVER_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Welcome to the Miner Bot! Click 'Open' to access the mining interface:",
        reply_markup=reply_markup,
    )

# راه‌اندازی بات تلگرام
def run_bot():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

# راه‌اندازی Flask و بات
if __name__ == "__main__":
    import threading

    # اجرای بات تلگرام در یک رشته جداگانه
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # اجرای اپلیکیشن Flask
    app.run(host="0.0.0.0", port=5000)
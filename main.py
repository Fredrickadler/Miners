from flask import Flask, render_template, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging

# تنظیمات بات تلگرام
TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"
bot = Bot(token=TOKEN)

# تنظیمات Flask
app = Flask(__name__)

# راه‌اندازی سیستم ثبت گزارش‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تنظیم Dispatcher برای مدیریت پیام‌ها
dispatcher = Dispatcher(bot, None, use_context=True)

# تعریف دستور /start
def start(update: Update, context):
    update.message.reply_text("Welcome to the Miner Bot! Let's start mining!")

# تعریف مدیریت پیام‌های متنی
def echo(update: Update, context):
    update.message.reply_text(f"You said: {update.message.text}")

# افزودن دستور و مدیریت پیام‌ها به Dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# مسیر اصلی وب‌سرور برای نمایش صفحه اصلی
@app.route('/')
def index():
    return render_template('index.html')

# دریافت پیام‌های وب‌هوک از تلگرام
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, bot)
    dispatcher.process_update(update)
    return "OK"

# تنظیم وب‌هوک هنگام اجرای سرور
@app.before_first_request
def setup_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=f"https://miner-p53z.onrender.com/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, render_template
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher
from telegram.ext import CallbackContext

# توکن ربات تلگرام خود را وارد کنید
TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"

# ساخت اپلیکیشن Flask
app = Flask(__name__)

# ساخت بات تلگرام
bot = Bot(token=TOKEN)

# تنظیم دیسپچِر
dispatcher = Dispatcher(bot, None, workers=0)

# فرمان شروع ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎉 Welcome to the Miner Bot! Let's mine together!")

# افزودن فرمان‌های ربات
dispatcher.add_handler(CommandHandler("start", start))

# رندر کردن صفحه اصلی
@app.route('/')
def index():
    return render_template('index.html')

# دریافت پیام‌های وب‌هوک از تلگرام
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# تنظیم وب‌هوک و اجرای سرور Flask
if name == "__main__":
    # تنظیم وب‌هوک
    bot.set_webhook(url=f"https://your-server-url.com/{TOKEN}")  # آدرس سرور خود را جایگزین کنید
    # اجرای سرور Flask
    app.run(host="0.0.0.0", port=5000)
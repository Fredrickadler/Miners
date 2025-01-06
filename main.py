from flask import Flask, render_template, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher
import threading

# --- تنظیمات توکن ---
TELEGRAM_BOT_TOKEN = "توکن_ربات_خود_را_اینجا_قرار_دهید"
WEBHOOK_URL = "https://miners-1.onrender.com"  # آدرس دامنه یا هاست

# --- راه‌اندازی اپلیکیشن ---
app = Flask(__name__)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# --- متغیرهای ساده ---
balance = 0
energy = 100
mining_status = "Waiting"
mined_blocks = []
current_block = {
    "number": 0,
    "reward": 0,
    "difficulty": 0,
}

# --- توابع مربوط به استخراج ---
def start_mining():
    global mining_status, mined_blocks, balance
    mining_status = "Mining"
    for i in range(1, 6):  # به‌عنوان مثال استخراج ۵ بلوک
        block = {
            "number": i,
            "reward": 100,
            "difficulty": 10 + i,
        }
        mined_blocks.append(block)
        balance += block["reward"]
    mining_status = "Completed"

@app.route("/")
def index():
    global balance, energy, mining_status, mined_blocks
    return render_template(
        "index.html",
        balance=balance,
        energy=energy,
        mining_status=mining_status,
        mined_blocks=mined_blocks,
    )

@app.route("/start-mining", methods=["POST"])
def start_mining_api():
    mining_thread = threading.Thread(target=start_mining)
    mining_thread.start()
    return "Mining started!"

# --- توابع مربوط به ربات ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Miner Bot! Use /web to open the miner interface.")

def web(update: Update, context: CallbackContext):
    update.message.reply_text(f"Open the Miner Web Interface: {WEBHOOK_URL}")

def setup_telegram_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("web", web))
    updater.start_polling()

# --- اجرای ربات ---
telegram_thread = threading.Thread(target=setup_telegram_bot)
telegram_thread.start()

# --- اجرای وب ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
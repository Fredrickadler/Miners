from flask import Flask, render_template, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4'
WEBHOOK_URL = 'https://miners-1.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# اطلاعات پیش‌فرض
user_data = {
    "balance": 1924.141,
    "energy": 24050,
    "mined_blocks": 0,
    "total_blocks": 100,
    "block_reward": 1237,
    "hash_rate": 0,
}

@app.route('/')
def index():
    return render_template('index.html', user_data=user_data)

@app.route('/start', methods=['POST'])
def start_mining():
    user_data["hash_rate"] += 10  # هش ریت مثال
    user_data["mined_blocks"] += 1
    user_data["balance"] += user_data["block_reward"]
    return "Mining started!"

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton('🛠 Start Mining', url=WEBHOOK_URL)
    markup.add(button)
    bot.send_message(chat_id, "Welcome to Miner Bot! Click below to start mining.", reply_markup=markup)

# تنظیم وب‌هوک
@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    return '', 200

@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'{WEBHOOK_URL}/webhook')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
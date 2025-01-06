from flask import Flask, render_template, request, jsonify
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
import json

app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# User data
users = {}

# Initialize data
def load_data():
    global users
    try:
        with open('data.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

def save_data():
    with open('data.json', 'w') as file:
        json.dump(users, file)

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/api/start_mining', methods=['POST'])
def start_mining():
    user_id = request.json.get('user_id')
    if user_id in users:
        users[user_id]['blocks_mined'] += 1
        users[user_id]['balance'] += users[user_id]['reward_per_block']
        save_data()
        return jsonify({'success': True, 'message': 'Mining started!'})
    return jsonify({'success': False, 'message': 'User not found'})

# Telegram Bot Handlers
def start(update: Update, context):
    user_id = str(update.message.chat_id)
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'energy': 100,
            'blocks_mined': 0,
            'reward_per_block': 10
        }
        save_data()

    keyboard = [
        [InlineKeyboardButton("Start Mining", callback_data='start_mining')],
        [InlineKeyboardButton("Upgrade", callback_data='upgrade')],
        [InlineKeyboardButton("Wallet", callback_data='wallet')],
        [InlineKeyboardButton("Stats", callback_data='stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to Miner Bot!", reply_markup=reply_markup)

def button_handler(update: Update, context):
    query = update.callback_query
    user_id = str(query.message.chat_id)

    if query.data == 'start_mining':
        if users[user_id]['energy'] > 0:
            users[user_id]['blocks_mined'] += 1
            users[user_id]['balance'] += users[user_id]['reward_per_block']
            users[user_id]['energy'] -= 10
            query.edit_message_text(f"Mining started! Blocks mined: {users[user_id]['blocks_mined']}")
        else:
            query.edit_message_text("Not enough energy!")
    elif query.data == 'wallet':
        query.edit_message_text(f"Balance: {users[user_id]['balance']} tokens")
    elif query.data == 'stats':
        query.edit_message_text(f"Stats:\nBalance: {users[user_id]['balance']} tokens\nBlocks mined: {users[user_id]['blocks_mined']}\nEnergy: {users[user_id]['energy']}")
    elif query.data == 'upgrade':
        query.edit_message_text("Upgrade functionality coming soon!")

    save_data()

# Telegram Bot Setup
def setup_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()

if __name__ == '__main__':
    load_data()
    setup_bot()
    app.run(debug=True)
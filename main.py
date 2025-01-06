from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# تنظیمات توکن و URL
BOT_TOKEN = "7745473410:AAFUmUC79yPnUV4-3IgpxPVnFFHsCLW7sD4"  # توکن ربات
WEBHOOK_URL = "https://miners-1.onrender.com"  # URL وب‌هوک

# تنظیم وب‌هوک برای ربات تلگرام
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    payload = {"url": f"{WEBHOOK_URL}/webhook"}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("وب‌هوک با موفقیت تنظیم شد.")
    else:
        print(f"خطا در تنظیم وب‌هوک: {response.text}")

set_webhook()

@app.route('/')
def index():
    return render_template('index.html')  # فایل index.html باید در پوشه templates باشد

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "Welcome to the Miner Bot!\nClick 'Open' below to start mining.")
    return "OK"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
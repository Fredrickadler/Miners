from flask import Flask, render_template, request, redirect, url_for
import telebot

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"  # جایگزین با توکن بات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

@app.route("/")
def loading_page():
    return render_template("loading.html")

@app.route("/payment")
def payment():
    # لینک پرداخت را ایجاد کنید
    payment_url = f"https://t.me/{bot.get_me().username}?start=payment_500stars"
    return redirect(payment_url)

@app.route("/success")
def success():
    return "پرداخت موفقیت‌آمیز بود! اکنون به صفحه اصلی دسترسی دارید."

if __name__ == "__main__":
    app.run(debug=True)
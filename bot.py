from flask import Flask, request, jsonify
import telebot
import requests
import json

BOT_TOKEN = "8773180444:AAFqH82a0WHIm6U2RG4knBUG1W2vBvJnSTI"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# بيانات الطلاب (يمكنك إضافة المزيد)
STUDENTS = {
    "أحمد محمد": "123456",
    "محمد علي": "234567",
    "عبدالله عمر": "345678",
}

# معالج رسائل البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎓 أرسل اسمك الكامل لاسترجاع الكود")

@bot.message_handler(func=lambda message: True)
def get_code(message):
    name = message.text.strip()
    
    if name in STUDENTS:
        code = STUDENTS[name]
        bot.reply_to(message, f"✅ مرحباً {name}\n🔑 كودك: {code}")
    else:
        bot.reply_to(message, f"❌ لم يتم العثور على: {name}")

# نقطة استقبال Webhook من تليجرام
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

# صفحة رئيسية للتحقق
@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "bot": "@student1jilelomaah_bot",
        "students": len(STUDENTS)
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
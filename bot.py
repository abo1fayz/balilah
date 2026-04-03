import telebot

BOT_TOKEN = "8773180444:AAFqH82a0WHIm6U2RG4knBUG1W2vBvJnSTI"

bot = telebot.TeleBot(BOT_TOKEN)

# حذف أي Webhook سابق
bot.remove_webhook()

# بيانات الطلاب
STUDENTS = {
    "أحمد محمد": "123456",
    "محمد علي": "234567",
    "عبدالله عمر": "345678",
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
🎓 *بوت استرجاع كود الطالب*

أرسل اسمك الكامل لاسترجاع الكود

📝 مثال: أحمد محمد
""", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def get_code(message):
    name = message.text.strip()
    
    if name in STUDENTS:
        code = STUDENTS[name]
        bot.reply_to(message, f"✅ مرحباً {name}\n🔑 كودك: `{code}`", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ لم يتم العثور على: {name}\n\nتأكد من كتابة الاسم كاملاً")

print("🤖 البوت يعمل...")
bot.infinity_polling()
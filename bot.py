import telebot
import firebase_admin
from firebase_admin import credentials, firestore
import re

BOT_TOKEN = "8773180444:AAFqH82a0WHIm6U2RG4knBUG1W2vBvJnSTI"

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()

# ========== الاتصال بـ Firebase ==========
# ضع المسار الصحيح لملف المفاتيح
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("✅ Firebase connected successfully")

# دالة لتنظيف النص
def normalize_text(text):
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('آ', 'ا').replace('إ', 'ا').replace('أ', 'ا')
    text = text.replace('ى', 'ي').replace('ة', 'ه')
    return text

# دالة للبحث عن الطالب
def search_student(name):
    try:
        students_ref = db.collection('students')
        docs = students_ref.get()
        
        normalized_search = normalize_text(name)
        
        for doc in docs:
            student = doc.to_dict()
            student_name = student.get('name', '')
            normalized_name = normalize_text(student_name)
            
            if normalized_name == normalized_search or normalized_search in normalized_name:
                return student
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
🎓 *بوت استرجاع كود الطالب - معهد جيل الأمة*

🔍 أرسل اسمك الكامل لاسترجاع الكود

📝 مثال: أحمد محمد
""", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def get_code(message):
    name = message.text.strip()
    
    if name.startswith('/'):
        return
    
    if len(name) < 3:
        bot.reply_to(message, "❌ الاسم قصير جداً")
        return
    
    student = search_student(name)
    
    if student:
        bot.reply_to(message, f"""
✅ *مرحباً {student.get('name')}*

🔑 *كودك:* `{student.get('code')}`

🔗 https://ommah3.vercel.app
""", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ لم يتم العثور على: {name}")

print("🤖 البوت يعمل...")
bot.infinity_polling()
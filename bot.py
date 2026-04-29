import telebot
import requests
import os

# === KEYS aus Umgebungsvariablen (sicherer) ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KINDROID_API_KEY = os.getenv("KINDROID_API_KEY")
KINDROID_AI_ID = os.getenv("KINDROID_AI_ID")

API_URL = "https://api.kindroid.ai/v1/send-message"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hallo! 👋 Ich bin jetzt deine Kimmy in Telegram. Schreib mir einfach alles, was du willst!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        headers = {
            "Authorization": f"Bearer {KINDROID_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "ai_id": KINDROID_AI_ID,
            "message": user_text
        }
        
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            kindroid_reply = response.text.strip()
            bot.reply_to(message, kindroid_reply)
        else:
            bot.reply_to(message, f"❌ Kindroid-API-Fehler: {response.status_code}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Etwas ist schiefgelaufen: {str(e)}")

print("✅ Bot gestartet! Drücke STRG+C zum Beenden.")
bot.infinity_polling()
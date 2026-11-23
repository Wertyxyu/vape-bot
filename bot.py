from telebot.apihelper import ApiTelegramException
import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask
import threading

# ==========================================
# ВАШИ ДАННЫЕ
TOKEN = os.getenv('BOT_TOKEN')

ADMIN_ID =  9138028220
# ==========================================

bot = telebot.TeleBot(TOKEN)
# ВСТАВЬ СЮДА ЮЗЕРНЕЙМ ТВОЕГО КАНАЛА (например, '@gustoy_batya_channel')
CHANNEL_ID = '@Gustoy_Batya'

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ('left', 'kicked'):
            return False
        return True
    except Exception:
        return False
app = Flask(__name__)

@bot.message_handler(content_types=['web_app_data'])
def handle_order(message):
    try:
        data = json.loads(message.web_app_data.data)
        text = f"🚨 **НОВЫЙ ЗАКАЗ!**\n\n"
        text += f"👤 От: {message.from_user.first_name} (@{message.from_user.username})\n"
        text += f"🛒 **Товары:**\n"
        for item in data['items']:
            text += f"• {item}\n"
        text += f"\n💰 **Сумма:** {data['total']} ₽\n"
        text += f"🏷 **Промокод:** {data['promo']}"
        bot.send_message(ADMIN_ID, text, parse_mode='Markdown')
        bot.send_message(message.chat.id, "✅ Ваш заказ принят!")
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Проверяем подписку
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "👋 Привет! Чтобы получить доступ к магазину, подпишись на наш канал: " + CHANNEL_ID)
        return # Если не подписан — дальше не идем
        
    # Если подписан — показываем приветствие
    bot.reply_to(message, "👋 Добро пожаловать в Gustoy_Batya!\n\nЧтобы открыть магазин, напишите /shop или нажмите на кнопку меню ниже.")
    
@bot.message_handler(commands=['shop'])
def send_shop_button(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo(url="https://wertyxyu.github.io/my-app/")
    markup.add(KeyboardButton(text="🛒 Открыть магазин", web_app=web_app))
    bot.send_message(message.chat.id, "Нажмите кнопку ниже:", reply_markup=markup)

def run_bot():
    print("Бот запущен...")
    bot.infinity_polling()

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

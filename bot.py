import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask
import threading

# ==========================================
# ВАШИ ДАННЫЕ
TOKEN = '9280671675:AAHZhECeDRH1OjhNT2ueIT2rEnaksH1Go8Y'  # Ваш настоящий токен
ADMIN_ID = 8688469208   # ВСТАВЬТЕ СВОЙ ID ОТ @userinfobot
# ==========================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 1. Обработчик заказов из Mini App
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

# 2. Команда /shop
@bot.message_handler(commands=['shop'])
def send_shop_button(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # ВСТАВЬТЕ СЮДА ССЫЛКУ НА ВАШ МАГАЗИН
    web_app = WebAppInfo(url="https://wertyxyu.github.io/my-app/")
    markup.add(KeyboardButton(text="🛒 Открыть магазин", web_app=web_app))
    bot.send_message(message.chat.id, "Нажмите кнопку ниже:", reply_markup=markup)

# 3. Запуск бота в фоне
def run_bot():
    print("Бот запущен...")
    bot.infinity_polling()

# 4. Заглушка для веб-сервера (чтобы Render дал бесплатный тариф)
@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    # Запускаем бота
    t = threading.Thread(target=run_bot)
    t.start()
    
    # Запускаем веб-сервер
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

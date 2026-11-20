import telebot
import json

# ВСТАВЬТЕ ВАШ ТОКЕН ОТ BOTFATHER (в кавычках)
TOKEN = '9280671675:AAHZhECeDRH1OjhNT2ueIT2rEnaksH1Go8Y'

# ВСТАВЬТЕ ВАШ ID (число без кавычек)
ADMIN_ID =  8688469208 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['web_app_data'])
def handle_order(message):
    try:
        # Получаем данные от Mini App
        data = json.loads(message.web_app_data.data)
        
        # Формируем текст для админа
        text = f"🚨 **НОВЫЙ ЗАКАЗ!**\n\n"
        text += f"👤 От: {message.from_user.first_name} (@{message.from_user.username})\n"
        text += f"🆔 ID клиента: `{message.from_user.id}`\n\n"
        text += f"🛒 **Товары:**\n"
        for item in data['items']:
            text += f"• {item}\n"
        
        text += f"\n💰 **Сумма:** {data['total']} ₽\n"
        text += f"🏷 **Промокод:** {data['promo']}"
        
        # Отправляем сообщение вам
        bot.send_message(ADMIN_ID, text, parse_mode='Markdown')
        
        # Отправляем ответ клиенту
        bot.send_message(message.chat.id, "✅ Ваш заказ принят! Админ свяжется с вами.")
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Ошибка при обработке заказа.")

print("Бот-админ запущен и ждет заказов...")
bot.infinity_polling()
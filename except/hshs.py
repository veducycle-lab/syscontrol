import telegram
from telegram.ext import Updater, MessageHandler, filters
import openai
import os

TELEGRAM_BOT_TOKEN = '6198647689:AAEw7nrS23Gh_o0Pd35xgxi8pRcyQFzpba0'
OPENAI_API_KEY = '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'

# Инициализация бота и OpenAI API
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
openai.api_key = OPENAI_API_KEY

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для генерации текста.")

# Обработчик сообщений от пользователя
def generate_text(update, context):
    # Получаем сообщение от пользователя
    user_message = update.message.text

    # Генерируем ответ с помощью OpenAI API
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_message,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Отправляем ответ пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

# Создаем обработчики команд и сообщений
start_handler = MessageHandler(filters.command & filters.regex('^/start$'), start)
generate_text_handler = MessageHandler(filters.text & (~filters.command), generate_text)

# Добавляем обработчики в бота
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(generate_text_handler)

# Запускаем бота
updater.start_polling()
updater.idle()

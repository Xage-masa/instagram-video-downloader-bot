import logging
import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Функция скачивания видео через парсинг страницы Instagram
def download_instagram_video_direct(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find("meta", property="og:video")
        if video_tag and video_tag.get("content"):
            video_url = video_tag.get("content")
            video_content = requests.get(video_url, headers=headers).content
            return video_content
        else:
            return None
    except Exception as e:
        logging.error(f"Ошибка при скачивании видео: {e}")
        return None

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне ссылку на видео в Instagram, и я скачаю его для тебя.")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "instagram.com" in text:
        await update.message.reply_text("Пробую скачать видео... Подожди пару секунд!")
        video = download_instagram_video_direct(text)
        if video:
            await update.message.reply_video(video)
        else:
            await update.message.reply_text("Не удалось найти видео по этой ссылке. Возможно, ссылка неправильная или видео недоступно.")
    else:
        await update.message.reply_text("Пожалуйста, отправь ссылку на пост или Reels из Instagram.")

# Основная функция запуска
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


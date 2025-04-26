import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Функция скачивания видео через RapidAPI
def download_instagram_video_api(insta_url):
    url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
    }
    querystring = {"url": insta_url}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        video_url = data.get('media')
        if video_url:
            video_content = requests.get(video_url).content
            return video_content
        else:
            return None
    except Exception as e:
        logging.error(f"Ошибка при обращении к API: {e}")
        return None

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне ссылку на пост или Reels из Instagram, и я скачаю видео для тебя.")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "instagram.com" in text:
        await update.message.reply_text("Пробую скачать видео...")
        video = download_instagram_video_api(text)
        if video:
            await update.message.reply_video(video)
        else:
            await update.message.reply_text("Не удалось найти видео. Проверь ссылку или попробуй позже.")
    else:
        await update.message.reply_text("Пожалуйста, отправь правильную ссылку на Instagram пост или Reels.")

# Основная функция запуска
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
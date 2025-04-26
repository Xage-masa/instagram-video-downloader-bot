# Instagram Video Downloader Bot

Telegram-бот для скачивания видео из постов и Reels в Instagram.  
Работает напрямую через парсинг страниц Instagram без использования сторонних сервисов.

---

##  Возможности

- Скачивает видео из обычных постов Instagram.
- Поддерживает Reels.
- Отправляет видео сразу пользователю в Telegram без сохранения на сервере.

---

##  Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/Xage-masa/instagram-video-downloader-bot.git
cd instagram-video-downloader-bot
```

2. Установить зависимости:

```bash
pip install -r requirements.txt
```

3. Создать файл `.env` и добавить в него свой токен бота:

```
TELEGRAM_TOKEN=ваш_токен_от_BotFather
```

4. Запустить бота:

```bash
python3 bot.py
```

---

##  Развертывание на Railway

- Подключить репозиторий.
- Установить переменные окружения:
  - `TELEGRAM_TOKEN`
- Railway сам определит запуск через `Procfile`.

---

##  Используемые технологии

- Python
- python-telegram-bot
- requests
- BeautifulSoup4

---

## Автор

Создано с любовью для практики и пользы.  
Telegram: @xagee

---


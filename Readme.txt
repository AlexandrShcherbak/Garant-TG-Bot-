Настройка проекта:

1) Скопируйте шаблон переменных окружения:
   cp .env.example .env

2) Откройте .env и заполните значения:
   - ADMIN_ID — ваш Telegram user id (число)
   - BOT_NAME — username бота без символа @
   - BOT_TOKEN — токен от BotFather

3) Установите зависимости:
   pip install -r requirements.txt

4) Запуск:
   python main.py

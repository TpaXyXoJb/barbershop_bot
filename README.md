# ✂ Telegram Bot для парикмахерской

Бот для записи клиентов в парикмахерскую с поддержкой PostgreSQL, Redis, Alembic, Celery, Docker и асинхронного стека на Python.

## 📦 Стек технологий
- Python 3.12 + aiogram
- PostgreSQL + SQLAlchemy (async)
- Alembic (async)
- Redis + Celery
- Docker + docker-compose
- Poetry

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий и перейди в директорию
```bash
git clone https://github.com/yourname/hit-haircut-bot.git
cd hit-haircut-bot
```

### 2. Создай `.env` в корне:
```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/bot_db
REDIS_URL=redis://redis:6379/0
BOT_TOKEN=your-telegram-bot-token
```

### 3. Запусти проект:
```bash
docker-compose up --build
```

---

## 🛠 Полезные команды

📌 Создание миграции:
```bash
docker-compose exec bot poetry run alembic revision --autogenerate -m "Initial migration"
```

📌 Применение миграций:
```bash
docker-compose exec bot poetry run alembic upgrade head
```

📌 Запуск тестов:
```bash
poetry run pytest
```

---

## 📂 Структура проекта

```
bot/
├── handlers/         # Хэндлеры бота
├── services/         # Логика и работа с API DIKIDI
├── models/           # SQLAlchemy-модели
├── database/         # Подключение и сессия
├── utils/            # Вспомогательные функции
├── config.py         # Переменные окружения
├── main.py           # Точка входа
├── tasks.py          # Celery задачи

migrations/           # Alembic (асинхронный)
tests/                # Тесты
Dockerfile            # Сборка контейнера
docker-compose.yml    # Сервисы
pyproject.toml        # Poetry
```

---

## 🧪 Тесты и данные
Для тестирования используется:
- `pytest`
- `factory-boy`

Тесты находятся в директории `tests/`. Покрытие тестами будет расширяться.

---

## 📌 Авторизация и роли
- ID владельца и мастеров задаются в `config.py`
- Поддержка ролей: клиент, мастер, владелец

---

## 📬 Обратная связь
Если есть вопросы или предложения — welcome в Issues / Pull Requests!

---

_Проект в разработке. Основной функционал реализуется пошагово._


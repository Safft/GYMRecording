# GYMRecording - API для отслеживания тренировок

## Описание проекта
**GYMRecording** - это API-сервис, разработанный с использованием **FastAPI** и **PostgreSQL**, позволяющий пользователям регистрироваться, входить в систему и отслеживать свои тренировки.

## Архитектура проекта

Проект использует модульную архитектуру, разделяя код на несколько основных компонентов:

- **`main.py`** - точка входа в приложение.
- **`app/alembic`** - миграции базы данных.
- **`app/DBSettings`** - настройки базы данных, модели SQLAlchemy и схемы Pydantic.
- **`app/routers`** - маршруты API, включая аутентификацию и управление тренировками.
- **`app/settings`** - файлы конфигурации, зависимости и логирование.
- **`docs/requirements.txt`** - список зависимостей проекта.
- **`Dockerfile` и `docker-compose.yml`** - конфигурации для контейнеризации приложения.

## Запуск проекта

1. **Клонирование репозитория**
```sh
 git clone https://github.com/Safft/GYMRecording.git
 cd GYMnotes
```

2. **Запуск через Docker**
```sh
docker-compose up --build
```

3. **Запуск без Docker** (нужно создать виртуальное окружение)
```sh
python -m venv .venv
source .venv\Scripts\activate
pip install -r docs/requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

## Доступные эндпоинты

### Аутентификация (`/auth`)
- `POST /auth/register/` - регистрация нового пользователя
- `POST /auth/token` - вход в систему и получение JWT-токена
- `DELETE /auth/delete/` - удаление аккаунта
- `PUT /auth/update/` - обновление имени пользователя
- `GET /auth/me/` - получение информации о текущем пользователе

### Тренировки (`/exercises`)
- `POST /exercises/` - добавить новую тренировку
- `GET /exercises/` - получить список всех тренировок пользователя
- `DELETE /exercises/{record_id}` - удалить тренировку
- `PUT /exercises/{record_id}` - обновить тренировку
- `GET /exercises/stats` - получить статистику тренировок (количество, средний вес, количество повторений)

### Типы упражнений (`/exercises/types`)
- `POST /exercises/types/` - добавить новое упражнение в базу
- `GET /exercises/types/` - получить список всех доступных упражнений

## Переменные окружения (`.env`)

Создайте `.env` файл в корне проекта и добавьте в него:
```ini
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=
SECRET_KEY=your_secret_key
SCHEMES=
ALGORITHM=
```

## Используемые технологии
- **FastAPI** - Фреймворк для API
- **PostgreSQL** - база данных
- **SQLAlchemy + Alembic** - ORM и миграции
- **Docker + Docker Compose** - контейнеризация
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер
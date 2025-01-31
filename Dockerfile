# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r docs/requirements.txt

ENV PYTHONUNBUFFERED=1

# Открываем порт приложения
EXPOSE 8000

# Запускаем FastAPI-приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

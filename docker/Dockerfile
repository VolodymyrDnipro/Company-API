# Базовый образ
FROM python:3.10

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование зависимостей в контейнер
COPY .env requirements.txt /app/

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта в контейнер
COPY . /app

# Открытие порта, на котором работает ваше приложение
EXPOSE 8000

# Команда, выполняемая при запуске контейнера
CMD ["python", "main.py"]
# Command to run the tests
CMD ["pytest"]

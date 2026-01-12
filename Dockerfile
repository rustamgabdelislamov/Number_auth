# Указываем базовый образ
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Копируем файл pyproject.toml и poetry.lock, если он есть
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry
RUN pip install poetry
RUN pip install gunicorn
# Устанавливаем зависимости проекта без создания виртуального окружения
RUN poetry config virtualenvs.create false
RUN poetry install --no-root -v
RUN gunicorn --version
# Копируем остальные файлы проекта в контейнер
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# CMD ["sh", "-c", "python manage.py collectstatic --no-input && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]

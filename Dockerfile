FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Создаем пользователя без прав root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Открываем порт для gunicorn
EXPOSE 9000

# Команда запуска
CMD ["gunicorn", "TaskTracker.wsgi:application", "--bind", "0.0.0.0:9000", "--workers", "4", "--timeout", "60", "--max-requests", "1000", "--max-requests-jitter", "100", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"] 
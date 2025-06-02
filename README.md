# TaskTracker

Система управления задачами на базе Django с Docker-контейнеризацией.

## Особенности

- Django 5.0+
- PostgreSQL в качестве базы данных
- Docker и Docker Compose для контейнеризации
- Монтирование томов для разработки без пересборки контейнера
- Поддержка переменных окружения через python-dotenv
- Автоматизированная настройка виртуального окружения

## Структура проекта

```
TaskTracker/
├── docker-compose.yml      # Конфигурация Docker Compose
├── Dockerfile              # Инструкции для сборки Docker-образа
├── requirements.txt        # Зависимости проекта
├── .env.example            # Пример файла с переменными окружения
├── .gitignore              # Файлы, игнорируемые Git
├── manage.py               # Утилита командной строки Django
├── static/                 # Статические файлы (CSS, JS, изображения)
├── media/                  # Загружаемые пользователем файлы
├── templates/              # Общие шаблоны проекта
├── tasks/                  # Приложение для управления задачами
│   ├── migrations/         # Миграции базы данных
│   ├── admin.py            # Настройки админ-панели
│   ├── apps.py             # Конфигурация приложения
│   ├── models.py           # Модели данных
│   ├── tests.py            # Тесты
│   └── views.py            # Представления
└── TaskTracker/            # Основной пакет проекта Django
    ├── settings.py         # Настройки проекта
    ├── urls.py             # Маршруты URL
    ├── wsgi.py             # Конфигурация WSGI
    └── asgi.py             # Конфигурация ASGI
```

## Начало работы

### Предварительные требования

- Docker и Docker Compose для запуска с Docker
- Python 3.11 или выше для локальной разработки

### Установка и запуск с Docker

1. Клонируйте репозиторий:
   ```
   git clone <url-репозитория>
   cd TaskTracker
   ```

2. Создайте файл .env на основе .env.example:
   ```
   cp .env.example .env
   ```

3. Запустите проект с помощью Docker Compose:
   ```
   docker-compose up -d
   ```

4. Приложение будет доступно по адресу: http://localhost:8000

### Локальная разработка

1. Создайте виртуальное окружение:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   ```

2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

3. Создайте файл .env с настройками для локальной разработки:
   ```
   cp .env.example .env
   ```

4. Выполните миграции и запустите сервер:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

## Тестирование

Для запуска тестов выполните:
```
python manage.py test
```

## Лицензия

MIT 
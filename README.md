# API Server with JWT Authentication

## Структура репозитория

1. **tests/** — Папка с тестами для проекта
2. **core/** — Основная настройка проекта
3. **app/** — Приложение для работы с пациентами
4. **docker/** — Папка с файлами Docker для контейнеризации
5. **requirements.txt** - Файл со всеми библиотеками

## Инструкции по локальному запуску

### Шаг 1: Клонирование репозитория

Сначала клонируйте репозиторий:

```bash
git clone https://your-repository-url.git
cd your-repository
```

### Шаг 2: Установка зависимостей

1. Убедитесь, что у вас установлен Python 3.11+ и Docker.

2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate  # Для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

### Шаг 3: Запуск проекта с помощью Docker

Для удобства проект настроен для запуска через Docker. Чтобы запустить проект в контейнере, выполните следующие шаги:

1. Создайте и запустите контейнеры:

```bash
docker-compose up --build
```

2. После этого проект будет доступен на http://localhost:8000.

### Шаг 4: Настройка базы данных и миграции

1. После того как контейнеры запустятся, выполните миграции для создания таблиц в базе данных:

```bash
docker-compose exec django python manage.py migrate
```

2. Cоздать суперпользователя для доступа к админ-панели:

```bash
docker-compose exec django python manage.py createsuperuser
```

### Шаг 5: Запуск тестов

Для запуска тестов, выполните следующую команду:

```bash
pytest
```

### Шаг 6: Работа с админ-панелью

1. Для того, чтобы получить доступ к админ-панели, откройте браузер и перейдите по следующему адресу:

```bash
http://localhost:8000/admin/
```

2. Войдите с учетными данными суперпользователя, которые вы создали на шаге 4.

### Шаг 7: Отправка запросов через Postman или cURL

Эндпоинт /login
Чтобы получить JWT токен, отправьте POST-запрос на /api/v1/login/ с телом запроса:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Ответ будет содержать токен:

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

Эндпоинт /patients
Чтобы получить список пациентов, отправьте GET-запрос на /api/v1/patients/patients/ с заголовком авторизации:

```bash
Authorization: Bearer your_access_token
```
Если у вас есть роль doctor, вы получите список пациентов в ответе:

```json
[
  {
    "id": 1,
    "date_of_birth": "1990-01-01",
    "diagnoses": [
      "Disease 1",
      "Disease 2"
    ],
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```
Если вы не в группе doctor, вы получите статус 403 (Access denied: only doctors are allowed.).

Пример запроса через cURL:
```bash
curl -X GET "http://localhost:8000/api/patients/patients/" -H "Authorization: Bearer your_access_token"
```

## Структура проекта
**core/**
   - ***settings.py*** — Основные настройки Django проекта
   - ***urls.py*** — Главный файл маршрутизации для проекта
   - ***wsgi.py*** — Настройка WSGI для работы с Gunicorn

**app/**
   - ***apps.py*** — Конфигурация приложения
   - ***models.py*** — Модели для работы с пациентами
   - ***serializers.py*** — Сериализаторы для преобразования данных в JSON
   - ***views.py*** — Представления для обработки запросов
   - ***urls.py*** — Маршруты для эндпоинтов, связанных с пациентами
   - ***admin.py*** — Настройки для админ-панели

**docker/**
   - ***Dockerfile*** — Docker-конфигурация для создания контейнера
   - ***docker-compose.yaml*** — Конфигурация для запуска всех сервисов в Docker

**requirements.txt** - Содержит список всех зависимостей Python для проекта

**pytest.ini** - Конфигурационный файл для pytest, в котором могут быть заданы настройки для тестирования

**.gitignore** - Содержит список файлов и директорий, которые не должны попадать в репозиторий

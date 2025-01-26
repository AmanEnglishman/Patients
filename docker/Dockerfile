FROM python:3.11

WORKDIR /usr/src/app

# Копируем только необходимые файлы
COPY requirementsDocker.txt ./

# Устанавливаем нужные пакеты
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Сборка статики
RUN python manage.py collectstatic --noinput

# Команда для запуска сервера
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

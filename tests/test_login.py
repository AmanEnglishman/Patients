import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_success():
    # Создаем пользователя
    User.objects.create_user(username='doctor', password='password123')
    client = APIClient()

    # Отправляем POST-запрос на /login
    response = client.post('/api/v1/login/', {
        'username': 'doctor',
        'password': 'password123'
    }, format='json')

    # Проверяем успешный статус и наличие токенов
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_login_invalid_credentials():
    client = APIClient()

    # Отправляем POST-запрос с неверными учетными данными
    response = client.post('/api/v1/login/', {
        'username': 'gigi',
        'password': 'gaga'
    }, format='json')

    # Проверяем статус ошибки и сообщение
    assert response.status_code == 401
    assert response.data['detail'] == 'Invalid username or password'


@pytest.mark.django_db
def test_login_missing_fields():
    client = APIClient()

    # Отправляем POST-запрос с отсутствующими данными
    response = client.post('/api/v1/login/', {}, format='json')

    # Проверяем статус ошибки и сообщение
    assert response.status_code == 400
    assert 'username' in response.data
    assert 'password' in response.data

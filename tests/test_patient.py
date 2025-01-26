from django.contrib.auth.models import User, Group
from patients.models import Patient
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_patients_success():
    # Создаем группу doctor
    doctor_group, _ = Group.objects.get_or_create(name='doctor')

    # Создаем пользователя с ролью doctor
    user = User.objects.create_user(username='doctor', password='password123')
    user.groups.add(doctor_group)

    # Создаем записи пациентов
    Patient.objects.create(date_of_birth="1990-01-01", diagnoses=["Diagnosis 1"])
    Patient.objects.create(date_of_birth="1985-06-15", diagnoses=["Diagnosis 2", "Diagnosis 3"])

    client = APIClient()

    # Логинимся и получаем токен
    login_response = client.post('/api/v1/login/', {
        'username': 'doctor',
        'password': 'password123'
    }, format='json')
    access_token = login_response.data['access']

    # Устанавливаем токен в заголовке Authorization
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Отправляем GET-запрос на /patients
    response = client.get('/api/v1/patients/')

    # Проверяем успешный статус и данные пациентов
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['diagnoses'] == ["Diagnosis 1"]


@pytest.mark.django_db
def test_patients_forbidden():
    # Создаем пользователя без роли doctor
    User.objects.create_user(username='nurse', password='password123')

    client = APIClient()

    # Логинимся и получаем токен
    login_response = client.post('/api/v1/login/', {
        'username': 'nurse',
        'password': 'password123'
    }, format='json')
    access_token = login_response.data['access']

    # Устанавливаем токен в заголовке Authorization
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Отправляем GET-запрос на /patients
    response = client.get('/api/v1/patients/')

    # Проверяем статус ошибки доступа
    assert response.status_code == 403
    assert response.data['detail'] == 'Access denied: only doctors are allowed.'


@pytest.mark.django_db
def test_patients_unauthenticated():
    client = APIClient()

    # Отправляем GET-запрос на /patients без токена
    response = client.get('/api/v1/patients/')

    # Проверяем статус ошибки аутентификации
    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'

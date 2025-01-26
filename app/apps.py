from django.apps import AppConfig


class AppPatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # Создаем роль doctor, если его нет при запуске проекта
    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='doctor')





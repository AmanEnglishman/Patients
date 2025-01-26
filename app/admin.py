from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'diagnoses',
        'created_at',
        'date_of_birth'
    )

from django.db import models


class Patient(models.Model):
    date_of_birth = models.DateField()
    diagnoses = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient {self.id}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

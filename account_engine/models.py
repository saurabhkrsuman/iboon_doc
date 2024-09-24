from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    PATIENT = "Patient"
    DOCTOR = "Doctor"
    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patients', limit_choices_to={'role': 'Doctor'})

    def __str__(self):
        return self.user.username

class Prescription(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prescriptions', limit_choices_to={'role': 'Doctor'})
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    details = models.TextField()
    
    def __str__(self) -> str:
        return f'Prescription for {self.patient.user.username}'

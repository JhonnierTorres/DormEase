from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superuser', 'Superuser'),
        ('ra', 'Resident Assistant'),
        ('resident', 'Resident'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='resident',
    )

    def __str__(self):
        return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Custom User Model with Resident Details
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('ra', 'Resident Assistant'),
        ('superuser', 'Superuser'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    move_in_date = models.DateField(blank=True, null=True)

# Room Model for Assignments
class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=1)
    occupants = models.ManyToManyField(CustomUser, related_name='assigned_room', blank=True)

    def is_full(self):
        return self.occupants.count() >= self.capacity
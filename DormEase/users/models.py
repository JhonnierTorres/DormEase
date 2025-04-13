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

    CHECK_IN_CHOICES = [
        ('pending', 'Pending'),
        ('checked_in', 'Checked In'),
    ]
    check_in_status = models.CharField(max_length=20, choices=CHECK_IN_CHOICES, default='pending')

# Room Model for Assignments
# models.py
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('quad', 'Quad'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    occupants = models.ManyToManyField('CustomUser', blank=True, related_name='assigned_room')

    def is_full(self):
        return self.occupants.count() >= self.capacity

    def __str__(self):
        return f"{self.room_number} ({self.room_type})"

    

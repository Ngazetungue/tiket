from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

USER_TYPE_CHOICES = [
    ('staff', 'Staff'),
    ('admin', 'Admin'),
    ('organiser', 'Organiser'),
]

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='staff')
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


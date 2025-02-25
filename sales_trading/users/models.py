from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trader', 'Trader'),
        ('sales', 'Sales Representative'),
        ('customer', 'Customer'),
    ]
    
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    # сreated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class CV(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

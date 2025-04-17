from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Experience(models.Model):
    parsed_resume = models.ForeignKey('ParsedResume', related_name='experiences', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    responsibilities = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.title} ({self.duration})"

class ParsedResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.user.email} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

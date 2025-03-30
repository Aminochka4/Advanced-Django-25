from django.contrib.auth.models import User 
from django.db import models

class Category(models.Model): 
    name = models.CharField(max_length=100) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        return self.name 

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Добавили null=True, blank=True
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(default="No description")

    def __str__(self): 
        return f"{self.user.username if self.user else 'No User'} - {self.amount}"

class GroupExpense(models.Model): 
    name = models.CharField(max_length=255) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.DateField() 
    users = models.ManyToManyField(User)
     
    def split_expense(self): 
        return self.amount / self.users.count() 
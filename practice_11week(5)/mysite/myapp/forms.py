from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'category', 'amount', 'description']  # Убедись, что здесь правильные поля

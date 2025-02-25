from django import forms
from .models import BuyOrder

class BuyOrderForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = ['product', 'quantity']

from django.db import models
from products.models import Product
from users.models import UserProfile

class BuyOrder(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buy_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BuyOrder {self.id} - {self.product.name} by {self.buyer.username}"

class SellOrder(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sell_orders')
    buy_order = models.OneToOneField(BuyOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SellOrder {self.id} - {self.buy_order.product.name} by {self.seller.username}"

class Transaction(models.Model):
    buy_order = models.OneToOneField(BuyOrder, on_delete=models.CASCADE)
    sell_order = models.OneToOneField(SellOrder, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.buy_order.product.name}"

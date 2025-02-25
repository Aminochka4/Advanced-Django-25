from django.contrib import admin
from .models import BuyOrder, SellOrder, Transaction

@admin.register(BuyOrder)
class BuyOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'product__name')

@admin.register(SellOrder)
class SellOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy_order', 'seller', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('seller__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy_order', 'sell_order', 'total_price', 'timestamp')
    search_fields = ('buy_order__product__name',)

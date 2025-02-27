from django.db.models.signals import post_save
from django.dispatch import receiver
from sales.models import Transaction
from .models import TradeAnalytics
from django.utils.timezone import now

@receiver(post_save, sender=Transaction)
def update_trade_analytics(sender, instance, created, **kwargs):
    if created:  # Только для новых сделок
        today = now().date()
        analytics, _ = TradeAnalytics.objects.get_or_create(date=today)

        analytics.total_trades += 1
        analytics.total_revenue += instance.total_price  # Учитываем общую сумму сделки
        analytics.trading_volume += instance.quantity  # Добавляем к объёму торговли
        analytics.profit_loss += instance.total_price - instance.product.cost_price * instance.quantity  # Вычисляем P/L

        analytics.save()

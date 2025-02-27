from django.db import models
from django.utils.timezone import now

class TradeAnalytics(models.Model):
    date = models.DateField(default=now)  # Дата для анализа трендов
    total_trades = models.PositiveIntegerField(default=0)  # Общее количество сделок
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Общая выручка
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Прибыль/убыток
    trading_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Объём торговли

    def __str__(self):
        return f"Analytics ({self.date}): Trades {self.total_trades}, Revenue {self.total_revenue}"

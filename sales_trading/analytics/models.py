from django.db import models

class TradeAnalytics(models.Model):
    total_trades = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Analytics: Trades {self.total_trades}, Revenue {self.total_revenue}"


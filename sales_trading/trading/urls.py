from django.urls import path
from .views import buy_order_list, accept_buy_order

urlpatterns = [
    path('buy-orders/', buy_order_list, name='buy_order_list'),
    path('buy-orders/<int:buy_order_id>/accept/', accept_buy_order, name='accept_buy_order'),
]

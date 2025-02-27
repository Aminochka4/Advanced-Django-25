from django.urls import path
from .views import create_buy_order, buy_order_list, accept_buy_order, user_orders

urlpatterns = [
    path('buy-orders/', buy_order_list, name='buy_order_list'),
    path('buy-orders/<int:buy_order_id>/accept/', accept_buy_order, name='accept_buy_order'),
    path('my-orders/', user_orders, name='user_orders'),
    path('buy/<int:product_id>/', create_buy_order, name='create_buy_order'),  # Добавлено
]

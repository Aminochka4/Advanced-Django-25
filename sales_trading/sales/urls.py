from django.urls import path
from .views import confirm_delivery, pay_invoice, seller_orders, user_orders

urlpatterns = [
    path('pay-invoice/<int:order_id>/', pay_invoice, name='pay_invoice'),\
    path('confirm-delivery/<int:order_id>/', confirm_delivery, name='confirm_delivery'),
    path('seller-orders/', seller_orders, name='seller_orders'),
    path('user-orders/', user_orders, name='user_orders'),
]
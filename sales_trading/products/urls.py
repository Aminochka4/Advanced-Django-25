from django.urls import path
from .views import product_list, add_product, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('<int:product_id>/', product_detail, name='product_detail'),
]

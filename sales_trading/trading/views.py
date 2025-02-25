from django.shortcuts import render, redirect, get_object_or_404
from .models import BuyOrder, Product, SellOrder, Transaction
from .forms import BuyOrderForm
from sales.models import SalesOrder
from django.contrib.auth.decorators import login_required

def create_buy_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = BuyOrderForm(request.POST)
        if form.is_valid():
            buy_order = form.save(commit=False)
            buy_order.buyer = request.user
            buy_order.status = 'pending'
            buy_order.save()
            return redirect('buy_order_success')
    else:
        form = BuyOrderForm(initial={'product': product})
    
    return render(request, 'trading/create_buy_order.html', {'form': form, 'product': product})

def accept_buy_order(request, buy_order_id):
    buy_order = get_object_or_404(BuyOrder, id=buy_order_id)

    if buy_order.status != 'pending':
        return redirect('error_page')  # Ошибка, если заказ уже обработан
    
    # Создаём SellOrder
    sell_order = SellOrder.objects.create(
        seller=buy_order.product.seller,  # Нужно добавить seller в Product
        buy_order=buy_order,
        status='pending'
    )

    # Создаём Transaction
    transaction = Transaction.objects.create(
        buy_order=buy_order,
        sell_order=sell_order,
        total_price=buy_order.total_price()
    )

    # Создаём SalesOrder
    SalesOrder.objects.create(
        transaction=transaction,
        final_price=transaction.total_price
    )

    # Обновляем статус BuyOrder
    buy_order.status = 'accepted'
    buy_order.save()

    return redirect('order_success')

@login_required
def buy_order_list(request):
    seller = request.user
    buy_orders = BuyOrder.objects.filter(product__seller=seller, status='pending')  # Заказы только на товары продавца
    return render(request, 'trading/buy_order_list.html', {'buy_orders': buy_orders})


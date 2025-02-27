from django.shortcuts import render, redirect, get_object_or_404
from .models import BuyOrder, Product, SellOrder, Transaction
from .forms import BuyOrderForm
from sales.models import SalesOrder
from django.contrib.auth.decorators import login_required

@login_required
def create_buy_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = BuyOrderForm(request.POST)
        if form.is_valid():
            buy_order = form.save(commit=False)
            buy_order.buyer = request.user  # Получаем профиль пользователя
            buy_order.status = 'pending'
            buy_order.save()
            return redirect('product_list')
    else:
        form = BuyOrderForm(initial={'product': product})
    
    return render(request, 'trading/create_buy_order.html', {'form': form, 'product': product})

@login_required
def accept_buy_order(request, buy_order_id):
    buy_order = get_object_or_404(BuyOrder, id=buy_order_id)

    if buy_order.status != 'pending':
        return redirect('error_page')  # Ошибка, если заказ уже обработан

    # Проверяем, есть ли уже SellOrder для этого BuyOrder
    existing_sell_order = SellOrder.objects.filter(buy_order=buy_order).first()
    if existing_sell_order:
        return redirect('error_page')  # Ошибка, если уже есть SellOrder

    # Создаём SellOrder
    sell_order = SellOrder.objects.create(
        seller=buy_order.product.seller,
        buy_order=buy_order,
        status='pending'
    )

    # Создаём Transaction
    total_price = buy_order.quantity * buy_order.product.price
    transaction = Transaction.objects.create(
        buy_order=buy_order,
        sell_order=sell_order,
        total_price=total_price
    )

    # Создаём SalesOrder
    SalesOrder.objects.create(
        transaction=transaction,
        final_price=transaction.total_price
    )

    # Обновляем статус BuyOrder
    buy_order.status = 'accepted'
    buy_order.save()

    return redirect('buy_order_list')


@login_required
def buy_order_list(request):
    seller = request.user
    buy_orders = BuyOrder.objects.filter(product__seller=seller, status='pending')  # Заказы только на товары продавца
    return render(request, 'trading/buy_order_list.html', {'buy_orders': buy_orders})

@login_required
def user_orders(request):
    user = request.user.userprofile
    orders = SalesOrder.objects.filter(transaction__buy_order__buyer=user)
    return render(request, 'trading/user_orders.html', {'orders': orders})


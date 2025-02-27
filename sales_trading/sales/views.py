from django.shortcuts import get_object_or_404, redirect, render
from .models import Invoice, SalesOrder
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta

@login_required
def pay_invoice(request, order_id):
    sales_order = get_object_or_404(SalesOrder, id=order_id, transaction__buy_order__buyer=request.user)

    # Создаём Invoice, если его нет, и сразу добавляем due_date
    invoice, created = Invoice.objects.get_or_create(
        sales_order=sales_order,
        defaults={'due_date': now() + timedelta(days=30)}  # Устанавливаем due_date
    )

    if not invoice.is_paid:  # Если ещё не оплачен, то оплачиваем
        invoice.is_paid = True
        invoice.save()

        sales_order.status = 'paid'
        sales_order.save()

    return redirect('user_orders')

@login_required
def confirm_delivery(request, order_id):
    sales_order = get_object_or_404(SalesOrder, id=order_id, transaction__sell_order__seller=request.user)

    if sales_order.status == 'paid':
        sales_order.status = 'complete'
        sales_order.save()

    return redirect('seller_orders')

@login_required
def seller_orders(request):
    seller = request.user
    orders = SalesOrder.objects.filter(transaction__sell_order__seller=seller)
    return render(request, 'sales/seller_orders.html', {'orders': orders})

@login_required
def user_orders(request):
    buyer = request.user
    orders = SalesOrder.objects.filter(transaction__buy_order__buyer=buyer)
    return render(request, 'sales/users_orders.html', {'orders': orders})



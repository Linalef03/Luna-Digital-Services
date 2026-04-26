from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import Order
from logs.utils import create_log


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.status = 'pending'
            order.save()

            create_log(request.user, f"Créer une nouvelle requête #{order.id}")

            messages.success(request, " La commande a été créée avec succès ! ")
            return redirect('orders:my_orders')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})

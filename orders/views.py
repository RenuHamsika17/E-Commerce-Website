from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    order = Order.objects.create(customer=request.user, total_price=cart.total_price())

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart.items.all().delete()
    messages.success(request, "Order placed successfully.")
    return redirect('dashboard')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # Update order status based on progression
    status_flow = ['Pending', 'Processing', 'Placed', 'Shipped', 'Out for Delivery']
    try:
        current_index = status_flow.index(order.status)
        if current_index < len(status_flow) - 1:
            order.status = status_flow[current_index + 1]
            order.save()
    except ValueError:
        pass  # if status is unknown, do nothing

    items = order.items.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})


@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tracking = order.tracking_updates.order_by('-updated_at')
    return render(request, 'orders/track_order.html', {
        'order': order,
        'tracking': tracking
    })


from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # You can enhance this to actually integrate Razorpay/Stripe
        order.status = 'Processing'  # or 'Paid' if payment gateway is used
        order.save()

        messages.success(request, f"Payment via {payment_method} received for Order #{order.id}.")
        return redirect('order_detail', order_id=order.id)

    return redirect('order_detail', order_id=order.id)



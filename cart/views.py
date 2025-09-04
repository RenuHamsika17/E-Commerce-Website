from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        messages.error(request, "Invalid quantity.")
        return redirect('product_detail', product_id=product.id)

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('product_detail', product_id=product.id)

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items in stock.")
        return redirect('product_detail', product_id=product.id)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    
    if cart_item:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.warning(request, f"Only {product.stock} in stock. You already have {cart_item.quantity} in cart.")
            return redirect('cart')
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            cart=cart,
            product=product,
            quantity=quantity,
            price_at_purchase=product.price  # required field
        )

    cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Dynamically calculate subtotal for each item
    for item in cart.items.all():
        item.subtotal = item.price_at_purchase * item.quantity

    return render(request, 'cart/cart_detail.html', {'cart': cart})

from .models import CartItem

@login_required
def update_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()  # remove item if quantity set to 0
        except ValueError:
            pass
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
    return redirect('cart')
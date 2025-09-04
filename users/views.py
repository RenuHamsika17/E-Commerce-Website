from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required

from users.models import User, Customer, Seller
from products.models import Product, Category
from orders.models import Order, OrderItem
from users.forms import CustomerProfileForm, SellerProfileForm


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    ROLE_CHOICES = [('customer', 'Customer'), ('seller', 'Seller')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('signup')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                is_customer=(role == 'customer'),
                is_seller=(role == 'seller')
            )

            if role == 'customer':
                Customer.objects.create(user=user, address="", phone_no="")
            else:
                Seller.objects.create(user=user, shop_name="", phone_no="")

            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # actually email
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # go to common dashboard
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_customer:
        try:
            customer = Customer.objects.get(user=user)
            context['profile'] = customer
            context['customer'] = customer
            context['orders'] = Order.objects.filter(customer=user).order_by('-order_date')
        except Customer.DoesNotExist:
            context['profile'] = None

    elif user.is_seller:
        try:
            seller = Seller.objects.get(user=user)
            context['profile'] = seller
            seller_products = Product.objects.filter(seller=user)
            context['seller_products'] = seller_products
            seller_orders = OrderItem.objects.filter(
                product__in=seller_products
            ).select_related('order', 'order__customer', 'product')
            context['seller_orders'] = seller_orders
        except Seller.DoesNotExist:
            context['profile'] = None
            context['seller_orders'] = None
            context['seller_products'] = None

    return render(request, 'users/dashboard.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if user.is_customer:
        profile = get_object_or_404(Customer, user=user)
        form_class = CustomerProfileForm
        role = 'customer'
    elif user.is_seller:
        profile = get_object_or_404(Seller, user=user)
        form_class = SellerProfileForm
        role = 'seller'
    else:
        messages.error(request, "Invalid user role.")
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'role': role,
    })


@login_required
def add_product(request):
    if not request.user.is_seller:
        messages.error(request, "You are not authorized to add products.")
        return redirect('dashboard')

    seller = Seller.objects.get(user=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        if name and price and stock and category_id:
            try:
                category = Category.objects.get(id=category_id)
                Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    stock=stock,
                    image=image,
                    seller=request.user,
                    category=category
                )
                messages.success(request, 'Product added successfully.')
                return redirect('dashboard')
            except Category.DoesNotExist:
                messages.error(request, "Selected category does not exist.")
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'products/add_product.html', {'categories': categories})

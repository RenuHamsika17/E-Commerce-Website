from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from users.models import User, Customer, Seller

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
        
# Sign-up view


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']

            # ✅ Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('signup')

            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                is_customer=(role == 'customer'),
                is_seller=(role == 'seller')
            )

            # Create profile
            if role == 'customer':
                Customer.objects.create(user=user, address="", phone_no="")
            else:
                Seller.objects.create(user=user, shop_name="", phone_no="")

            login(request, user)
            return redirect('login')  # or 'home' if you want to log them in directly

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'registration/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

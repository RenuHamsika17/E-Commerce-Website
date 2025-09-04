from django.contrib.auth.forms import UserCreationForm
from .models import User  # Custom user model
from django import forms
from users.models import Customer, Seller

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    ROLE_CHOICES = [('customer', 'Customer'), ('seller', 'Seller')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.first_name = self.cleaned_data.get('first_name')
        user.is_customer = (role == 'customer')
        user.is_seller = (role == 'seller')
        if commit:
            user.save()
        return user

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_no', 'address']
        widgets = {
            'phone_no': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-[#21284a] text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your phone number',
            }),
            'address': forms.Textarea(attrs={
                'class': 'mt-1 block w-full bg-[#21284a] text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Enter your address',
            }),
        }



class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['phone_no', 'shop_name']
        widgets = {
            'phone_no': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-[#21284a] text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'shop_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-[#21284a] text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', 'card_number', 'card_expiry', 'card_cvv']

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')
        if method == 'Card':
            if not cleaned_data.get('card_number') or not cleaned_data.get('card_expiry') or not cleaned_data.get('card_cvv'):
                raise forms.ValidationError("Card details are required for card payment.")


from django.contrib.auth.forms import UserCreationForm
from .models import User  # Custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

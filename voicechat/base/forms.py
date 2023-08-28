from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task  # Import your CustomUser model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
        
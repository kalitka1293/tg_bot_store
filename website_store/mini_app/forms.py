from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={
                'pattern': r'^\+?1?\d{9,15}$',
                'placeholder': '+79991234567'
            }),
        }
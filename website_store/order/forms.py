from django import forms
from order.models import Order
from django.core.validators import RegexValidator

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={
                'pattern': r'^\+?[\d\s\-()]{8,20}$|^(?:\+?\d\s?){6,14}\d$',
                'placeholder': '+7 999 123-45-67'
            }),
        }

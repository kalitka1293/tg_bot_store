from django import forms
from django.core.exceptions import ValidationError
from order.models import Order


class OrderCreateForm(forms.ModelForm):
    online_payment = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    callback_request = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (999) 123-45-67'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not all(c in '0123456789+()- ' or c.isalpha() for c in phone):
            raise ValidationError("Недопустимые символы в номере")
        phone = (phone.replace('+', '')
                 .replace('(', '')
                 .replace(')', '')
                 .replace('-', '').
                 replace(' ', ''))
        if len(phone) != 11:  # Проверка длины
            raise ValidationError("Длина номера должна быть 11")
        return phone

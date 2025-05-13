from django import forms
from django.core.cache import cache


class SearchForm(forms.Form):
    print(cache.get('brand_list'))
    brand = forms.ChoiceField(
        choices=cache.get('brand_list'),
        required=False,
    )
    country = forms.ChoiceField(
        choices=cache.get('country_list'),
        required=False
    )
    type_equipment = forms.ChoiceField(
        choices=cache.get('typeEquipment'),
        required=False
    )

    price__lt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                "class": 'price-input',
                                                                'placeholder': 'До',
                                                                'type': 'number',
                                                                'value': ''
                                                                }
                                                            ),
                                  required=False)
    price__gt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                "class": 'price-input',
                                                                'placeholder': 'От',
                                                                'type': 'number'
                                                                    }
                                                            ),
                                  required=False)

    cooling_power__gt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'От',
                                                                        'type': 'number'}
                                                                    ),
                                   required=False)
    cooling_power__lt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'До',
                                                                        'type': 'number'}
                                                                    ),
                                           required=False)
    heating_power__gt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'От',
                                                                        'type': 'number'}
                                                                    ),
                                           required=False)
    heating_power__lt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'До',
                                                                        'type': 'number'}
                                                                    ),
                                           required=False)
    working_area__gt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'От',
                                                                        'type': 'number'}
                                                                    ),
                                           required=False)
    working_area__lt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'До',
                                                                        'type': 'number'}
                                                                    ),
                                           required=False)
    sound_level__gt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'От',
                                                                        'type': 'number'}
                                                                    ),
                                          required=False)
    sound_level__lt = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                        "class": 'price-input',
                                                                        'placeholder': 'До',
                                                                        'type': 'number'}
                                                                    ),
                                          required=False)
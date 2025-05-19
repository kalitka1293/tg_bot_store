from django import forms
from django.core.cache import cache
from mini_app.redis import check_data_in_redis

def get_cache_param(key: str):
    data = cache.get(key)
    if data is None:
        print('\n\n')
        print('ключа нет')
        print('\n\n')
        check_data_in_redis()
        print(cache.get(key))
        print('\n\n')
        return cache.get(key)
    else:
        return data

class SearchForm(forms.Form):
    brand = forms.ChoiceField(
        choices=get_cache_param('brand_list'),
        required=False,
    )
    country = forms.ChoiceField(
        choices=get_cache_param('country_list'),
        required=False
    )
    type_equipment = forms.ChoiceField(
        choices=get_cache_param('typeEquipment'),
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
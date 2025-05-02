from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from mini_app.models import Product, Basket
from django.core.cache import cache

from mini_app.redis import download_product_all_redis

F = 'hat'

class TestTeplateView(TemplateView):
    template_name = f'mini_app/{F}.html'

class MainMenuView(ListView):
    template_name = 'mini_app/index.html'
    model = Product #redis
    paginate_by = 10


    def get_queryset(self):
        download_product_all_redis()
        return list(cache.get('products').values())

class ProductCardView(TemplateView):
    template_name = 'mini_app/product_card.html'

    def get_context_data(self, **kwargs):
        download_product_all_redis()
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        context['product_card'] = cache.get('products').get(product_id)
        print(context)
        return context

class BasketView(TemplateView):
    template_name = 'mini_app/basket.html'

    def get_context_data(self, **kwargs):
        user = 3434

        download_product_all_redis()
        context = super().get_context_data(**kwargs)
        list_id_product = Basket.objects.filter(user=user).values_list('product_id', 'quantity')
        list_product = []
        for item in list_id_product:
            product_id, product_quantity = str(item[0]), item[1]
            product = cache.get('products').get(product_id)
            product.update({'quantity': product_quantity, 'sum': product['price'] * product_quantity})
            list_product.append(product)
        context['products'] = list_product
        context['total_sum'] = self.get_total_sum(list_product)
        return context

    def get_total_sum(self, list_product: list):
        total_sum = 0
        for product in list_product:
            total_sum += product['price'] * product['quantity']
        return total_sum


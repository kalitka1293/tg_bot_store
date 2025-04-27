from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from mini_app.models import Product
from django.core.cache import cache

from mini_app.redis import download_product_all_redis


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

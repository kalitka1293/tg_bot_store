from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from mini_app.models import Product
from django.core.cache import cache


class MainMenuView(ListView):
    template_name = 'mini_app/index.html'
    model = Product #redis
    paginate_by = 10

    # from mini_app.redis import download_product_all_redis
    # download_product_all_redis()
    # print([i for i in cache.get('products')])
    # cache.clear()
    # def get_queryset(self):
    #     pass
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     pass

class ProductCardView(TemplateView):
    template_name = 'mini_app/product_card.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        context['list_peculiarity'] = None
        return None

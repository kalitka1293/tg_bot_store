from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from mini_app.redis import download_product_all_redis
from mini_app.models import Product, Article


F = 'test'

@csrf_exempt
def test_view(request):
    pass

class TestTemplateView(TemplateView):
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

class ArticleView(DetailView):
    template_name = 'mini_app/article.html'
    model = Article




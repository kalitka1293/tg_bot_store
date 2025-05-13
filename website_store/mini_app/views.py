from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from mini_app.filter import ProductSearch
from mini_app.forms import SearchForm
from mini_app.models import Article, Product
from mini_app.redis import download_product_all_redis

F = 'test_fastapi'


@csrf_exempt
def test_view(request):
    pass


class TestTemplateView(TemplateView):
    template_name = f'mini_app/{F}.html'


class MainMenuView(ListView):
    template_name = 'mini_app/index.html'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        if self.kwargs.get('param', False):
            if self.kwargs.get('param') == 'ShowPopup':
                context['showPopup'] = True
        return context

    def get_queryset(self):
        download_product_all_redis()
        s = cache.get('brand_list')
        assert s is not None
        return list(cache.get('products').values())


class ProductCardView(TemplateView):
    template_name = 'mini_app/product_card.html'

    def get_context_data(self, **kwargs):
        download_product_all_redis()
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        context['product_card'] = cache.get('products').get(product_id)
        print(context['product_card'])
        return context


class ArticleView(DetailView):
    template_name = 'mini_app/article.html'
    model = Article

    # Здесь добавить аналитику

class SearchView(ListView):
    template_name = 'mini_app/search.html'
    model = Product
    paginate_by = 6
    form = SearchForm
    filterset_class = ProductSearch
    context_object_name = 'product_list'

    def get_queryset(self):
        qs = super().get_queryset()
        data_request = self.update_get_data(dict(self.request.GET))
        self.data_request = data_request
        self.filterset = self.filterset_class(
            data=data_request,
            queryset=qs
        )
        if not self.filterset.is_valid():
            print("ОШИБКИ ФИЛЬТРАЦИИ:", self.filterset.errors)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(initial=self.data_request)
        return context

    def update_get_data(self, request_get) -> dict:
        """
        'brand': ['Ballu'], 'country': ['']
        ->
        {'brand': 'Ballu', 'price__lt': '1616'}
        Нормализуем данные, удаляем пустые значения, value=list -> value->str
        :param request_get: self.request.GET or request.GET
        :return: dict
        """
        iterable_dict = dict(request_get)
        dict_data = {}
        for key, value in iterable_dict.items():
            if not value[0]:
                continue
            dict_data.update({key: value[0]})
        return dict_data

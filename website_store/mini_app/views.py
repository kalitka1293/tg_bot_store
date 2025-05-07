from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from mini_app.redis import download_product_all_redis
from mini_app.models import Product, Basket, Article, Order
from mini_app.forms import OrderCreateForm

from common.webappTelegram import check_webapp_signature, parse_init_data

import json


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

@method_decorator(csrf_exempt, name='dispatch')
class BasketView(TemplateView):
    template_name = 'mini_app/basket.html'

    def post(self, request, *args, **kwargs):
        init_data = json.loads(request.body)['initData']

        #Токен убрать в безопасное место
        result = check_webapp_signature(init_data, '6938844148:AAGUItfOaLAUE2pjj9ZlGEe-BZeizNnoqJM')
        if not result:
            raise ValueError(init_data)
            #return JsonResponse({'status': 'Not valid'},status=403)
        data_user_telegram = parse_init_data(init_data)
        telegram_id = data_user_telegram['user']['id']
        # request['PATH_INFO'] = '/mini_app/article/2'
        # print(request['PATH_INFO'])
        return JsonResponse({'url': f'/mini_app/basket/{telegram_id}'})

    def get_context_data(self, **kwargs):
        user = kwargs.get('telegram_id')
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

class ArticleView(DetailView):
    template_name = 'mini_app/article.html'
    model = Article


class FormPayView(CreateView):
    model = Order
    template_name = 'mini_app/form_pay.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('mini_app:main_menu')
    # success_message = 'Ты успешно зарегистрирован!!!'


# class FormPayView(TemplateView):
#     template_name = 'mini_app/form_pay.html'


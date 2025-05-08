from rabbitmq_common_code.common.webappTelegram import check_webapp_signature, parse_init_data
from order.forms import OrderCreateForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.http import JsonResponse
from mini_app.redis import download_product_all_redis

from order.models import Order, Basket
import json

class FormPayView(CreateView):
    model = Order
    template_name = 'mini_app/form_pay.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('mini_app:main_menu')
    # success_message = 'Ты успешно зарегистрирован!!!'

class OrdersListView(ListView):
    template_name = 'mini_app/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)

class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
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
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from jwt_custom.service import JWTAuthorization
from mini_app.models import StoreUser
from mini_app.redis import download_product_all_redis
from order.forms import OrderCreateForm
from order.models import Basket, Order


class FormPayView(JWTAuthorization, CreateView):
    model = Order
    template_name = 'order/form_pay.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('mini_app:main_menu')
    # success_message = 'Ты успешно зарегистрирован!!!'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        # В данные передатьdsf

    def form_valid(self, form):
        online_payment = form.cleaned_data['online_payment']  # 1 или 0
        callback_request = form.cleaned_data['callback_request']
        if online_payment or not callback_request:
            form.instance.pay_type = 0
        elif not online_payment or callback_request:
            form.instance.pay_type = 1
        else:
            # Обработка ошибки
            form.pay_type = 0
            raise ValueError()
        form.instance.initiator = StoreUser.objects.get(telegram_id=self.telegram_id)
        return super().form_valid(form)


class OrdersListView(JWTAuthorization, ListView):
    template_name = 'order/orders.html'
    queryset = Order.objects.all()
    ordering = ('-id',)
    context_object_name = 'basket_history'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.telegram_id, '<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        print(queryset.filter(initiator=self.telegram_id))
        return queryset.filter(initiator=StoreUser.objects.get(telegram_id=self.telegram_id))


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context


@method_decorator(csrf_exempt, name='dispatch')
class BasketView(JWTAuthorization, TemplateView):
    template_name = 'order/basket.html'

    def get_context_data(self, **kwargs):
        user = self.telegram_id
        download_product_all_redis()  # Delete
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

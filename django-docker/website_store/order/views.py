from django.core.cache import cache
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from jwt_custom.service import JWTAuthorization
from mini_app.models import StoreUser
from mini_app.redis import download_product_all_redis
from mini_app.tasks import send_data_ordering_telegram_bot
from order.forms import OrderCreateForm
from order.models import Basket, Order


class FormPayView(JWTAuthorization, CreateView):
    model = Order
    template_name = 'order/form_pay.html'
    form_class = OrderCreateForm

    def get_success_url(self):
        return reverse('order:success_ordering', kwargs={'order_id': self.object.id})

    def form_valid(self, form):
        user_telegram = StoreUser.objects.get(telegram_id=self.telegram_id)
        # формирует читабельные данные и отправляет в rabbitmq
        self.create_message_for_telegram(form.cleaned_data.copy(), user_telegram)

        online_payment = form.cleaned_data['online_payment']  # 1 или 0
        callback_request = form.cleaned_data['callback_request']

        if online_payment or not callback_request:
            form.instance.pay_type = 0
        elif not online_payment or callback_request:
            form.instance.pay_type = 1
        else:
            # Обработка ошибки
            print(online_payment, callback_request,
                  'online_payment, callback_request', form.cleaned_data)
            form.instance.pay_type = 0
            raise ValueError()
        form.instance.initiator = user_telegram
        response = super().form_valid(form)
        return response

    def create_message_for_telegram(self, form_data: dict, user_telegram: StoreUser):
        send_data_tg = form_data
        basket_user = [item.de_json() for item in Basket.objects.filter(user=self.telegram_id)]

        text_basket_user = ''
        for product in basket_user:
            text_basket_user += '\n\nТовар:\n'
            for key, value in product.items():
                text_basket_user += f'{key}: {value}\n'

        send_data_tg.update(
            {
                'telegram_ID': self.telegram_id,
                'telegram_username': user_telegram.telegram_username,
                'telegram_first_name': user_telegram.telegram_first_name,
                'telegram_last_name': user_telegram.telegram_last_name,
                'Заказы': text_basket_user
            }
        )
        send_data_ordering_telegram_bot(send_data_tg)


class OrdersListView(JWTAuthorization, ListView):
    template_name = 'order/orders.html'
    queryset = Order.objects.all()
    ordering = ('-id',)
    context_object_name = 'basket_history'

    def get_queryset(self):
        queryset = super().get_queryset()
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


class SuccessOrderView(TemplateView):
    template_name = 'order/success_ordering.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        context['order_id'] = order_id
        return context

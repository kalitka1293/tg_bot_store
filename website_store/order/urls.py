from django.urls import path
from order.views import BasketView, FormPayView, OrdersListView

app_name = 'order'

urlpatterns = [
    path('form_pay/', FormPayView.as_view(), name='form_pay'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('orders_list/', OrdersListView.as_view(), name='orders_list'),
]

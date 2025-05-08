from django.urls import path
from order.views import FormPayView, BasketView

app_name = 'order'

urlpatterns = [
    path('form_pay/', FormPayView.as_view(), name='form_pay'),
    path('basket/<int:telegram_id>', BasketView.as_view(), name='basket'),
]


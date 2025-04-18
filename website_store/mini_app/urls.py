from django.urls import path
from mini_app.views import MainMenuView, ProductCardView

app_name = 'mini_app'

urlpatterns = [
    path('menu/', MainMenuView.as_view(), name='main_menu'),
    path('product/<int:product_id>', ProductCardView.as_view(), name='product_card'),
]
#<id:int>
from django.urls import path
from mini_app.views import MainMenuView, ProductCardView, TestTemplateView, ArticleView, test_view

app_name = 'mini_app'

urlpatterns = [
    path('menu/', MainMenuView.as_view(), name='main_menu'),
    path('product/<str:product_id>', ProductCardView.as_view(), name='product_card'),
    path('test_view/', TestTemplateView.as_view(), name='test_view'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('test/', test_view, name='test'),
]
#<id:int>
from django.urls import path
from mini_app.views import MainMenuView

app_name = 'mini_app'

urlpatterns = [
    path('menu/', MainMenuView.as_view(), name='main_menu')
]
from django.urls import path
from jwt_custom.views import set_cookie_view

app_name = 'token_jwt'

urlpatterns = [
    path('get/', set_cookie_view, name='get')
]
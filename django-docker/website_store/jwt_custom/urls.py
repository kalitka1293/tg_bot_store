from django.urls import path
from jwt_custom.views import ErrorAuthorizationView, set_cookie_view

app_name = 'token_jwt'

urlpatterns = [
    path('get/', set_cookie_view, name='get'),
    path('error/', ErrorAuthorizationView.as_view(), name='error_authorization'),
]

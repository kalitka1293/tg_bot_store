import json
from datetime import datetime, timedelta, timezone

import jwt
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from mini_app.models import StoreUser
from rabbitmq_common_code.common.webappTelegram import (check_webapp_signature,
                                                        parse_init_data)
from django.shortcuts import render

SECRET_KEY = settings.SECRET_KEY_JWT
ALGORITHM = settings.ALGORITHM
BOT_SECRET = settings.BOT_SECRET
ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA = timedelta(minutes=120)
SET_COOKIE_SECURE = settings.SET_COOKIE_SECURE


def custom_type_error_handler(request, exception=None):
    return render(request, "jwt_custom/error500.html", status=500)


def custom_type_error_handler_404(request, exception=None):
    return render(request, "jwt_custom/error404.html", status=404)


class ErrorAuthorizationView(TemplateView):
    template_name = 'jwt_custom/error_authorization_in_telegram.html'


@csrf_exempt
def set_cookie_view(request):
    initData = json.loads(request.body)['initData']
    result_check_initData = check_webapp_signature(initData, BOT_SECRET)
    if not result_check_initData:
        return HttpResponseRedirect(
            reverse('token_jwt:error_authorization')
        )
    telegram_id = parse_init_data(initData)
    if telegram_id is None or not telegram_id:
        return HttpResponseRedirect(
            reverse('token_jwt:error_authorization')
        )
    create_or_check_user(telegram_id)
    telegram_id = telegram_id['user']['id']
    # проверка, запись в бд
    token = create_access_token({"sub": str(telegram_id)})
    response = HttpResponse()
    response.set_cookie(
        key='Authorization',
        value=f"Bearer {token}",
        httponly=True,
        max_age=1000,
        samesite='lax',
        secure=SET_COOKIE_SECURE
    )
    return response


def create_or_check_user(data: dict):
    """
    Создает если пользователя нет
    Проверяет, есть ли пользователь в системе
    :param data: Данные пользователя
    :return: None
    """
    data = data['user']
    try:
        result = StoreUser.objects.filter(telegram_id=data['id']).exists()
        if not result:
            StoreUser.objects.create(telegram_id=data['id'],
                                     telegram_username=data['username'],
                                     telegram_first_name=data['first_name'],
                                     telegram_last_name=data['last_name'])
            return
        return
    except Exception as f:
        return HttpResponseRedirect(
            reverse('token_jwt:error_authorization')
        )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    telegram_id = payload.get('sub', None)
    if telegram_id is None:
        return None
    return telegram_id

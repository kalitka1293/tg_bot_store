import jwt
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

SECRET_KEY = 'd0c4381c2b040057974cbe8dbe4f051c595807abda2538b6e8f10eb71f09c1d9'
ALGORITHM = "HS256"


def validation_authorization_get_current_user(credentials: str | None):
    if credentials is None or not credentials.startswith('Bearer '):
        print('1')
        return False
    token = credentials.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as f:
        print('2')
        return False
    print(payload)
    telegram_id = payload.get('sub', None)
    if telegram_id is None:
        print('3')
        return False
    return int(telegram_id)


class JWTAuthorization:
    """
    Класс аутентификации пользователей,
    проверки подлености токенов и
    если пользователя нет в БД, доавбляет
    """

    def authorization_jwt(self, request):
        cookie = request.COOKIES.get('Authorization', None)
        result = validation_authorization_get_current_user(cookie)
        if not result or result is None:
            return HttpResponseRedirect(
                reverse('mini_app:main_menu_with_param',
                        kwargs={'param': 'ShowPopup'})
            )
        self.telegram_id = result

    def get(self, request, *args, **kwargs):
        redirect_response = self.authorization_jwt(request)
        if redirect_response:
            return redirect_response
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect_response = self.authorization_jwt(request)
        if redirect_response:
            return redirect_response
        return super().post(request, *args, **kwargs)

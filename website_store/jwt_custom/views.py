from django.shortcuts import render
from datetime import datetime, timedelta, timezone
import jwt
from django.http import HttpResponse
from rabbitmq_common_code.common.webappTelegram import check_webapp_signature, parse_init_data
from django.views.decorators.csrf import csrf_exempt

SECRET_KEY = 'd0c4381c2b040057974cbe8dbe4f051c595807abda2538b6e8f10eb71f09c1d9'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA = timedelta(minutes=15)
import json

@csrf_exempt
def set_cookie_view(request):
    initData = json.loads(request.body)['initData']
    # Токен убрать в безопасное место
    # result_check_initData = check_webapp_signature(initData, '6938844148:AAGUItfOaLAUE2pjj9ZlGEe-BZeizNnoqJM')
    # if not result_check_initData:
    #     raise
    print(initData, '<<<<<')
    telegram_id = parse_init_data(initData)
    telegram_id = telegram_id['user']['id']

    token = create_access_token({"sub": str(telegram_id)})
    response = HttpResponse()
    response.set_cookie(
        key='Authorization',
        value=f"Bearer {token}",
        httponly=True,
        max_age=1000,
        samesite='lax',
        secure=False
    )
    return response

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    telegram_id = payload.get('sub', None)
    if telegram_id is None:
        return None
    return telegram_id







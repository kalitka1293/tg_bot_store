from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dto.token_jwt import TelegramId
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
# from rabbitmq_common_code.common.webappTelegram import (check_webapp_signature,
#                                                         parse_init_data)

"""
"sub" = В данном случае является ключем для telegram_id но для безопастности
 мы не будем указывать что это telegram id 
"""

SECRET_KEY = 'd0c4381c2b040057974cbe8dbe4f051c595807abda2538b6e8f10eb71f09c1d9'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA = timedelta(hours=2)
cookie_scheme = APIKeyCookie(name="Authorization")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validation_authorization_get_current_user(token: Annotated[str, Depends(cookie_scheme)]) -> TelegramId:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not token.startswith('Bearer '):
        raise credentials_exception
    token = token.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as f:
        raise credentials_exception
    telegram_id = payload.get('sub', None)
    if telegram_id is None:
        raise credentials_exception
    return TelegramId(telegram_id=int(telegram_id))

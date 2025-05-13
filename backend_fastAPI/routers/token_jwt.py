# from typing import Annotated
#
# from dto.token_jwt import TelegramId
# from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
#                      status)
# from services.token_jwt import (ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA,
#                                 create_access_token,
#                                 validation_authorization_get_current_user)
#
# router_token = APIRouter()
# @router_token.put('/lol')
# async def data_test(credentials: Annotated[TelegramId, Depends(validation_authorization_get_current_user)]):
#     print(credentials)
#     print(credentials.telegram_id)
#     return credentials
# @router_token.post('/token')
# async def get_token_access(response: Response, form_data: InitData):
#     if form_data is None:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     # Валидация initData после успеха вернуть telegram_id
#     # function
#     access_token = create_access_token({"sub": form_data.initData})
#     token = Token(access_token=access_token, token_type='Bearer')
#
#     response.set_cookie(
#         key='access_token',
#         value=f"{token.token_type} {token.access_token}",
#         httponly=True,
#         max_age= datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_HOURS_TIMEDELTA,
#         samesite='lax',
#         secure=False
#         # secure=True if HTTPS
#     )
#     return {"message": "Successfully authenticated", 'status': status.HTTP_200_OK}
#
# @router_token.get('/item')
# async def get_data(request: Request):
#     # Depends разоюратся что это
#     print("Все заголовки запроса:")
#     for name, value in request.headers.items():
#         print(f"{name}: {value}")
#
#     # Выводим конкретные интересующие заголовки
#     print("\nВажные заголовки:")
#     print(f"User-Agent: {request.headers.get('user-agent')}")
#     print(f"Authorization: {request.headers.get('authorization')}")
#     print(f"Cookie: {request.headers.get('cookie')}")
#     print(f"Host: {request.headers.get('host')}")
#
#     # Выводим переданные куки (если есть)
#     print("\nКуки:")
#     cookies = request.cookies
#     for cookie_name, cookie_value in cookies.items():
#         print(f"{cookie_name}: {cookie_value}")
#
#     print("\nПолученные данные аутентификации:")
#     return {"message": "Successfully authenticated", 'status': status.HTTP_200_OK


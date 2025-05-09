import jwt
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
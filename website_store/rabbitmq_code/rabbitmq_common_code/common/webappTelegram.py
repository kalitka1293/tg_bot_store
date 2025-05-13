import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qs, parse_qsl


def check_webapp_signature(init_data: str, token: str) -> bool:
    """
    Check incoming WebApp init data signature
    :param token:
    :param init_data:
    :return: bool
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return calculated_hash == hash_


def parse_init_data(init_data: str) -> dict:
    parsed = parse_qs(init_data)
    result = {}

    for key, value in parsed.items():
        if key == 'user':
            result[key] = json.loads(value[0])
        else:
            result[key] = value[0] if len(value) == 1 else value

    return result
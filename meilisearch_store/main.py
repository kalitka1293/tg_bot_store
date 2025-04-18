from app import client
from dowload_data_meilisearch import add_one_data_product, add_all_data_product

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from rabbitmq_common_code.consumer import ConsumerRabbit
from rabbitmq_common_code.config_common import PRODUCT_MEILISEARCH, FASTAPI_QUEUE

import json


def search_meilisearch(ch, method, properties, body):
    body = json.loads(body)
    print(body)

    if body["type"] == 'add_product':
        add_one_data_product(body["index"], body["product_id"])
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    else:
        raise ValueError(f'body["type"] не определен {body}')

def main():
    add_all_data_product('product')
    consumer_rabbit = ConsumerRabbit(PRODUCT_MEILISEARCH, search_meilisearch)
    consumer_rabbit.consumer()

if __name__ == '__main__':
    main()




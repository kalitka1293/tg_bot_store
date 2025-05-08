from celery import shared_task


from rabbitmq_common_code.consumer import ConsumerRabbit
from rabbitmq_common_code.config_common import BASKET_QUEUE

from django.apps import apps

import json

def exaple_fun_consumer(ch, method, properties, body):
    body = json.loads(body)
    print(body)
    ...
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return

consumer_basket = ConsumerRabbit(BASKET_QUEUE, exaple_fun_consumer)

@shared_task
def consumer_basket_rabbit():
    print(apps.ready)
    if not apps.ready:
        print('Не запущен Rabbit')
        return
    consumer_basket.consumer()

consumer_basket_rabbit.delay()
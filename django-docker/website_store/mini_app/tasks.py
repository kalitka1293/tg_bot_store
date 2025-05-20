import json

from celery import shared_task
from django.apps import apps
from rabbitmq_common_code.config_common import BASKET_QUEUE
from rabbitmq_common_code.consumer import ConsumerRabbit
from rabbitmq_common_code.producer import ProducerRabbit


@shared_task
def send_data_ordering_telegram_bot(data_ordering: dict):
    """
    Функция отправки в брокер данных о заказе пользователя
    """
    text_message = ''
    for key, value in data_ordering.items():
        if key == 'callback_request' and value == 1:
            key = 'Способ оплаты'
            value = 'Связаться с клиентом'

        if key == 'online_payment' and value == 1:
            key = 'Способ оплаты'
            value = 'Онлайн оплата'

        text_message += f'{key}: {value}\n\n'
    producer = ProducerRabbit('tg_bot', 'fastapi_meilisearch') #fastapi_meilisearch это временная заглушка
    producer.producer({'message': text_message})
    print(f'Данные заказа: {data_ordering} отправлен в Rabbit в очередь: tg_bot')


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

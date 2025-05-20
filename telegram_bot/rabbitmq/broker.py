from rabbitmq_common_code.config_common import ConnectValidRabbit
from rabbitmq.send_channel_message import send_message_channel
import pika
import json
import datetime

async def consumer_tg():
    connect_param = ConnectValidRabbit('tg_bot', 'fastapi_meilisearch') #fastapi_meilisearch это временная заглушка
    connection = pika.BlockingConnection(connect_param.connection_param)
    channel = connection.channel()

    try:
        channel.queue_declare(queue='tg_bot', passive=True)
    except pika.exceptions.ChannelClosedByBroker:
        return

    method_frame, header_frame, body = channel.basic_get(connect_param.queue)

    if method_frame:
        try:
            data = json.loads(body)
            print("Получено сообщение:", data)
            if not data.get('message', False):
                print(data.get('message', False), 'пришли неверные данные')
                channel.basic_ack(method_frame.delivery_tag)
                return
            await send_message_channel(data.get('message', 'Заказ создан находиться в Базе Данных'))
            channel.basic_ack(method_frame.delivery_tag)
        except Exception as f:
            print(f)
    else:
        print(f"Сообщений нет {datetime.datetime.now()}")

    connection.close()


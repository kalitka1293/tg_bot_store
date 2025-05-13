import json

from pika import BlockingConnection, ConnectionParameters
from rabbitmq_common_code.config_common import BASKET_QUEUE, ConnectValidRabbit


def exaple_fun_consumer(ch, method, properties, body):
    body = json.loads(body)
    print(body)
    ...
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return

class ConsumerRabbit(ConnectValidRabbit):
    def __init__(self, queue: str,fun,schema=None, __class=None):
        super().__init__(queue, schema)
        self.fun = fun
    def consumer(self):
        with BlockingConnection(self.connection_param) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue=self.queue)
                ch.basic_consume(
                    queue=self.queue,
                    on_message_callback=self.fun,
                )
                print(f'Консьюмер запущен. Слушаю {self.queue}\nОжидание сообщений')
                ch.start_consuming()


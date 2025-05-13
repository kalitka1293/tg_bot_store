from pika import BlockingConnection, ConnectionParameters, BasicProperties
import json
from rabbitmq_common_code.config_common import BASKET_QUEUE, ConnectValidRabbit

class ProducerRabbit(ConnectValidRabbit):
    def __init__(self, queue: str, schema: str):
        super().__init__(queue, schema)

    def producer(self, message_data):
        self.validations(message_data)
        with BlockingConnection(self.connection_param) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue=self.queue)
                ch.basic_publish(
                    exchange="",
                    routing_key=self.queue,
                    body=json.dumps(message_data),
                    properties=BasicProperties(
                        content_type='application/json',
                        delivery_mode=2,
                    )
                )

# x = ProducerRabbit(BASKET_QUEUE,  BASKET_QUEUE)
# x.producer({'product_id': 1, 'user': 3434, 'quantity': 1, 'action': 12},)
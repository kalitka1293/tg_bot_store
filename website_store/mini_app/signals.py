from mini_app.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rabbitmq_common_code')))
from producer import ProducerRabbit
from config_common import PRODUCT_MEILISEARCH


@receiver(post_save, sender=Product)
def after_add_product_in_db(sender, instance, created, **kwargs):
    data = {
        "product_id": instance.id,
        "type":"add_product",
        "index":"product"
    }
    producer = ProducerRabbit(PRODUCT_MEILISEARCH, 'add_data_meiliseacrh')
    producer.producer(data)
    print(f'Товар: {instance} отправлен в Rabbit в очередь: {PRODUCT_MEILISEARCH}')

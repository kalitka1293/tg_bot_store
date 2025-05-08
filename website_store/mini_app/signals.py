from mini_app.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from rabbitmq_common_code.producer import ProducerRabbit
from rabbitmq_common_code.config_common import PRODUCT_MEILISEARCH


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

# @receiver(m2m_changed, sender=Product)
# def after_add_product_in_db(sender, instance, created, **kwargs):
#     return
#     data = {
#         "product_id": instance.id,
#         "type":"add_product",
#         "index":"product"
#     }
#     producer = ProducerRabbit(PRODUCT_MEILISEARCH, 'add_data_meiliseacrh')
#     producer.producer(data)
#     print(f'Товар: {instance} отправлен в Rabbit в очередь: {PRODUCT_MEILISEARCH}')
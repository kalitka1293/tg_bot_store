from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.utils import timezone
from mini_app.models import Product, StoreUser
from rabbitmq_common_code.config_common import PRODUCT_MEILISEARCH
from rabbitmq_common_code.producer import ProducerRabbit
from mini_app.redis import download_product_all_redis, search_parameters_redis

@receiver(post_init, sender=StoreUser)
def update_last_login(sender, instance, **kwargs):
    if instance.pk:
        instance.last_login = timezone.now()
        instance.save(update_fields=['last_login'])

@receiver(post_save, sender=Product)
def after_add_product_in_db(sender, instance, created, **kwargs):
    download_product_all_redis()
    search_parameters_redis()
    data = {
        "product_id": instance.id,
        "type": "add_product",
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

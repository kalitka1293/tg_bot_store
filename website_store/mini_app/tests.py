import time
from unittest.mock import MagicMock, patch

from celery.result import AsyncResult
from django.db.models.signals import post_save
from django.test import TestCase, override_settings
from mini_app.models import (Brand, Country, Product, SubcategoryProduct,
                             TypeEquipment)
from mini_app.signals import after_add_product_in_db
from mini_app.tasks import consumer_basket_rabbit


class CeleryBrokerRunningTest(TestCase):
    """
    Тест 1: Проверка, что Celery брокер запущен и задача ставится в очередь
    """
    def test_celery_broker_accepts_task(self):
        # Отправляем простую задачу в очередь
        async_result = consumer_basket_rabbit.delay()

        # Проверяем, что задача получила task_id
        self.assertIsNotNone(async_result.id, "Задача не получила task_id")

        # Проверяем, что задача не завершена сразу (т.е. брокер принимает задачу)
        self.assertFalse(async_result.ready(), "Задача завершилась сразу, возможно CELERY_TASK_ALWAYS_EAGER=True")

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class RabbitMQSignalSendingTest(TestCase):
    """
    Тест 3: Проверка, что сигнал post_save для Product вызывает отправку через RabbitMQ
    """

    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(brand="Test Brand")
        cls.country = Country.objects.create(country="Test Country")
        cls.subcategory = SubcategoryProduct.objects.create(subcategory_product="Test Subcategory")
        cls.type_equipment = TypeEquipment.objects.create(type_equipment="Test Type")

    def setUp(self):
        # Отключаем реальный сигнал и подключаем мок
        post_save.disconnect(after_add_product_in_db, sender=Product)

        self.producer_patcher = patch('mini_app.signals.ProducerRabbit')
        self.MockProducer = self.producer_patcher.start()
        self.mock_producer_instance = MagicMock()
        self.MockProducer.return_value = self.mock_producer_instance

        post_save.connect(after_add_product_in_db, sender=Product)

        self.test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "brand": self.brand,
            "view_main_menu": True,
            "price": 10000,
            "cooling_power": 2.5,
            "heating_power": 3.0,
            "working_area": 25.0,
            "sound_level": 45.5,
            "country": self.country,
            "group_product": self.subcategory,
            "type_equipment": self.type_equipment
        }

    def tearDown(self):
        self.producer_patcher.stop()
        post_save.disconnect(after_add_product_in_db, sender=Product)

    def test_signal_sends_message_to_rabbitmq_on_create(self):
        product = Product.objects.create(**self.test_data)

        self.MockProducer.assert_called_once_with('meilisearch', 'add_data_meiliseacrh')
        self.mock_producer_instance.producer.assert_called_once_with({
            "product_id": product.id,
            "type": "add_product",
            "index": "product"
        })

    def test_signal_sends_message_to_rabbitmq_on_update(self):
        product = Product.objects.create(**self.test_data)
        initial_call_count = self.mock_producer_instance.producer.call_count

        product.price = 20000
        product.save()

        # Проверяем, что вызов увеличился (сигнал сработал при обновлении)
        self.assertEqual(
            self.mock_producer_instance.producer.call_count,
            initial_call_count + 1,
            "Сигнал не сработал при обновлении"
        )

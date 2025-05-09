from django.db import models
from django.core.validators import RegexValidator

from mini_app.models import Product


class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.IntegerField()
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.product.name

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS_CODE = (
        (CREATED, 'Coздан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Формат: '+999999999'. До 15 цифр."
        )
    ])
    address = models.CharField('Адрес', max_length=250)
    city = models.CharField('Город', max_length=100)
    created = models.DateTimeField('Создан', auto_now_add=True)
    # initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    basket_history = models.JSONField(default=dict)
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}, {self.created}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [item.de_json() for item in baskets],
            'total_sum': float(baskets.total_sum())
        }
        baskets.delete()
        self.save()


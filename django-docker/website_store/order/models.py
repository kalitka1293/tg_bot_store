from django.core.validators import RegexValidator
from django.db import models
from mini_app.models import Product, StoreUser


class BasketObjects(models.QuerySet):
    def total_sum(self):
        return sum([i.sum() for i in self])


class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.IntegerField()
    quantity = models.SmallIntegerField()

    objects = BasketObjects.as_manager()

    def __str__(self):
        return self.product.name

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_sum': float(self.sum())
        }
        return basket_item


class Order(models.Model):
    CREATED = 0
    PAID = 1
    STATUS_CODE = (
        (CREATED, 'Coздан'),
        (PAID, 'Оплачен'),
    )

    PAY_ONLINE = 0
    PAY_MANAGER = 1
    PAY_CODE = (
        (PAY_ONLINE, 'Оплата Онлайн'),
        (PAY_MANAGER, 'Оплата через менеджера'),
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
    initiator = models.ForeignKey(to=StoreUser, on_delete=models.CASCADE)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CODE)
    pay_type = models.SmallIntegerField(choices=PAY_CODE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}, {self.created}'

    def update_after_pay(self):
        """
        Удаляем данные из корзины пользователя после оплаты
        :return:
        """
        baskets = Basket.objects.filter(user=self.initiator.telegram_id)
        self.status = self.PAID
        baskets.delete()
        self.save()

    def update_payment_basket_history(self):
        """
        Добавляем данные из корзины, который пользователь выбрал
        перед оплатой
        :return:
        """
        baskets = Basket.objects.filter(user=self.initiator.telegram_id)
        self.basket_history = {
            'purchased_items': [item.de_json() for item in baskets],
            'total_sum': float(baskets.total_sum())
        }
        self.save()

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        baskets = Basket.objects.filter(user=self.initiator.telegram_id)
        self.basket_history = {
            'purchased_items': [item.de_json() for item in baskets],
            'total_sum': float(baskets.total_sum())
        }
        super().save(
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,)

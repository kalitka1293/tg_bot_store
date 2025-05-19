import uuid
from io import BytesIO

from django.core.files import File
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image


class StoreUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField()
    telegram_first_name = models.CharField(null=True, blank=True)
    telegram_last_name = models.CharField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)


class Country(models.Model):
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.country


class SubcategoryProduct(models.Model):
    subcategory_product = models.CharField(max_length=256)

    def __str__(self):
        return self.subcategory_product


class TypeEquipment(models.Model):
    type_equipment = models.CharField(max_length=256)

    def __str__(self):
        return self.type_equipment


class Brand(models.Model):
    brand = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.id} {self.brand}"


class Product(models.Model):
    """
    Установить CASCADE в on_delete
    """
    name = models.CharField(max_length=256)
    description = models.CharField()
    brand = models.ForeignKey(to=Brand, on_delete=models.DO_NOTHING)
    view_main_menu = models.BooleanField(default=False)
    price = models.IntegerField()
    cooling_power = models.FloatField()
    heating_power = models.FloatField()
    working_area = models.FloatField()
    sound_level = models.FloatField()
    country = models.ForeignKey(to=Country, on_delete=models.DO_NOTHING)
    group_product = models.ForeignKey(to=SubcategoryProduct, on_delete=models.DO_NOTHING)
    type_equipment = models.ForeignKey(to=TypeEquipment, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Удалять изображения при удалении товара
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products_images/',  # Папка для загрузки
        verbose_name='Изображение'
    )

    def generate_unique_name(self):
        return f"{uuid.uuid4().hex}.webp"

    def compress(self, image):
        img = Image.open(image)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        im_io = BytesIO()
        img.save(im_io, 'WEBP', quality=70, method=6)
        return File(im_io, name=image.name)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.image:  # Только если есть изображение
            # Генерация уникального имени перед сохранением
            original_name = self.image.name
            print('original_name', original_name, '\n\n')
            self.image.name = self.generate_unique_name()
            # Сжатие и оптимизация изображения
            compressed_image = self.compress(self.image)
            self.image.save(
                compressed_image.name,
                compressed_image.file,
                save=False
            )

        super().save(
      *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def __str__(self):
        return self.product.name


class ParameterProduct(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


class ReviewProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user_review_name = models.CharField()
    comment = models.CharField()
    rating = models.SmallIntegerField()


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    image = models.ImageField(upload_to='article/', verbose_name='Изображение статьи')
    content = CKEditor5Field(verbose_name='Полное описание', config_name='extends')
    show_counter = models.IntegerField(verbose_name='Счетчик показов статьи', null=True)

    def __str__(self):
        return self.title

from django.db import models
from django.core.files import File

from PIL import Image
import uuid
from io import BytesIO

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
        return self.brand

class Product(models.Model):
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


class ParameterProduct(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.key

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Удалять изображения при удалении товара
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products_images',  # Папка для загрузки
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
        update_fields=None,)



    def __str__(self):
        return self.product.name

class ReviewProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user_review_name = models.CharField()
    comment = models.CharField()
    rating = models.SmallIntegerField()

class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.IntegerField()
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.product.name

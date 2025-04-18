from django.db import models


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
    price = models.IntegerField()
    cooling_power = models.FloatField()
    heating_power = models.FloatField()
    working_area = models.FloatField()
    sound_level = models.FloatField()
    country = models.ForeignKey(to=Country, on_delete=models.DO_NOTHING)
    group_product = models.ForeignKey(to=SubcategoryProduct, on_delete=models.DO_NOTHING)
    type_equipment = models.ForeignKey(to=TypeEquipment, on_delete=models.DO_NOTHING)
    #Добавить отзывы
    #review =

    

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
    is_main = models.BooleanField(
        default=False,
        verbose_name='Главное изображение'
    )
    def __str__(self):
        return self.product.name


class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.IntegerField()
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.product.name

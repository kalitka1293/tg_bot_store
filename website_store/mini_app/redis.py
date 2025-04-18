from django.core.cache import cache
from mini_app.models import Product

def download_product_all_redis():
    result = Product.objects.all()

    dict_product = {}
    for product in result:
        dict_product[str(product)] = {
            'name': product.name,
        'description': product.description,
        'brand': product.brand.brand,
        'price': product.price,
        'cooling_power': product.cooling_power,
        'heating_power': product.heating_power,
        'working_area': product.working_area,
        'sound_level': product.sound_level,
        'country': product.country.country,
        'group_product': product.group_product.subcategory_product,
        'type_equipment': product.type_equipment.type_equipment,
        }
    cache.set('products', dict_product)
    dict_product.clear()
    return



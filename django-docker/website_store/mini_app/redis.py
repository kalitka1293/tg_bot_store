from django.core.cache import cache
from mini_app.models import (Brand, Country, ParameterProduct, Product,
                             ProductImage, ReviewProduct, TypeEquipment)


def check_data_in_redis():
    """
    Првоерка существований и содержания ключей redis
    """
    if cache.get('products') is None:
        print('NULL DATA IN REDIS products')
        download_product_all_redis()
    if cache.get('brand_list') is None:
        print('NULL DATA IN REDIS brand_list')
        search_parameters_redis()

def search_parameters_redis():
    print('== DOWNLOAD search_parameters_redis ==')
    brand_list = Brand.objects.all()
    country_list = Country.objects.all()
    typeEquipment = TypeEquipment.objects.all()

    brand_list = (('', ''),) + tuple([(i.brand, i.brand) for i in brand_list])
    country_list = (('', ''),) + tuple([(i.country, i.country) for i in country_list])
    typeEquipment = (('', ''),) + tuple([(i.type_equipment, i.type_equipment) for i in typeEquipment])

    cache.set('brand_list', brand_list, timeout=2 * 24 * 60 * 60)
    print(cache.get('brand_list'))
    cache.set('country_list', country_list, timeout=2 * 24 * 60 * 60)
    cache.set('typeEquipment', typeEquipment, timeout=2 * 24 * 60 * 60)
    return None


def download_product_all_redis():
    search_parameters_redis()

    result = Product.objects.all()
    dict_product = {}
    main_product = {}
    for product in result:
        product_data = {str(product.id): {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'brand': product.brand.brand,
            'price': product.price,
            'view_main_menu': product.view_main_menu,
            'cooling_power': product.cooling_power,
            'heating_power': product.heating_power,
            'working_area': product.working_area,
            'sound_level': product.sound_level,
            'country': product.country.country,
            'group_product': [{'id': str(item.id), 'working_area': item.working_area} for item in Product.objects.filter(group_product=product.group_product)],
            'type_equipment': product.type_equipment.type_equipment,
            'parameter_product': [{item.key: item.value} for item in ParameterProduct.objects.filter(product=product)],
            'review_product': [{"user_review_name": item.user_review_name, "comment": item.comment, "rating": item.rating}
                               for item in ReviewProduct.objects.filter(product=product)],
            'images_product': [item.image.url for item in ProductImage.objects.filter(product=product)]
            }
        }
        if product.view_main_menu:
            main_product.update(product_data)
        else:
            dict_product.update(product_data)

    main_product.update(dict_product)
    cache.set('products', main_product, timeout=2 * 24 * 60 * 60)
    main_product.clear()
    dict_product.clear()

    return None

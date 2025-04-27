from django.core.cache import cache
from mini_app.models import Product, ParameterProduct, ProductImage, ReviewProduct

def download_product_all_redis():
    result = Product.objects.all()
    group_product = {}
    dict_product = {}
    main_product = {}
    for product in result:
        product_data = {str(product.id):{
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
    cache.set('products', main_product)
    print(main_product)
    main_product.clear()
    dict_product.clear()

    return None





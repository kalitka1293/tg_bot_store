from django.contrib import admin
from mini_app.models import (Country, Product, ParameterProduct,
                             SubcategoryProduct, TypeEquipment, Brand,
                             Basket, ProductImage, ReviewProduct, Article,
                             Order)


admin.site.register(Basket)
admin.site.register(Country)
admin.site.register(ParameterProduct)
admin.site.register(SubcategoryProduct)
admin.site.register(TypeEquipment)
admin.site.register(Brand)
admin.site.register(Order)


class ReviewProductAdmin(admin.TabularInline):
    model = ReviewProduct
    extra = 1

class ParameterProductAdmin(admin.TabularInline):
    model = ParameterProduct
    fields = ('key', 'value',)
    extra = 1

class DownloadImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'group_product', 'id')
    fields = ('name','description','brand','price','cooling_power','heating_power',
              'working_area','sound_level','country','group_product',
              'type_equipment', 'view_main_menu',)
    inlines = (DownloadImageAdmin, ParameterProductAdmin, ReviewProductAdmin, )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'show_counter', )
    fields = ('title', 'image', 'content', )
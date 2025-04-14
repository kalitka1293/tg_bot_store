from django.contrib import admin
from mini_app.models import Country, Product, ParameterProduct, SubcategoryProduct, TypeEquipment, Brand, Basket


admin.site.register(Basket)
admin.site.register(Country)
admin.site.register(ParameterProduct)
admin.site.register(SubcategoryProduct)
admin.site.register(TypeEquipment)
admin.site.register(Brand)

class ParameterProductAdmin(admin.TabularInline):
    model = ParameterProduct
    fields = ('key', 'value',)
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'group_product')
    fields = ('name','description','brand','price','cooling_power','heating_power',
              'working_area','sound_level','country','group_product',
              'type_equipment',)
    inlines = (ParameterProductAdmin,)

from django.contrib import admin
from menu.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug', 'price', 'stock', 'available', 'sort', 'category']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available', 'sort']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(model_or_iterable=Category, admin_class=CategoryAdmin)
admin.site.register(model_or_iterable=Product, admin_class=ProductAdmin)

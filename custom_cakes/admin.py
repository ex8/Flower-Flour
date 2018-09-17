from django.contrib import admin
from custom_cakes.models import CustomCakeOrder, Cake, CustomCakeConfig, \
    CustomCakeOrderConfigOption, CustomCakeOrderConfigOptionItem


class CustomCakeConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner_image')
admin.site.register(CustomCakeConfig, CustomCakeConfigAdmin)


class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'small_description', 'image', 'available')
admin.site.register(Cake, CakeAdmin)


class CustomCakeAdmin(admin.ModelAdmin):
    list_display = ('date_needed', 'type', 'size', 'servings', 'complete', 'order')
    list_filter = ('type', 'size')
    list_editable = ('complete',)
admin.site.register(CustomCakeOrder, CustomCakeAdmin)


class CustomCakeOrderConfigOptionInline(admin.TabularInline):
    model = CustomCakeOrderConfigOptionItem
    extra = 0


class CustomCakeOrderConfigOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'form_type', 'sort', 'available')
    list_editable = ('sort', 'available')
    inlines = [CustomCakeOrderConfigOptionInline]
admin.site.register(CustomCakeOrderConfigOption, CustomCakeOrderConfigOptionAdmin)

from django.contrib import admin
from clover.models import Clover


class CloverAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'achieved')
admin.site.register(model_or_iterable=Clover, admin_class=CloverAdmin)

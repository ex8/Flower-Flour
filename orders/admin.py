from django.contrib import admin
from orders.models import Order, OrderItem, OrderConfig
import csv
import datetime
from django.http import HttpResponse


class OrderConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'list_banner_image', 'delivery_banner_image', 'custom_banner_image',
                    'create_banner_image')
admin.site.register(OrderConfig, OrderConfigAdmin)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
    filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    # no foreigns keys in model fields list
    fields = [field for field in opts.get_fields() if not field.many_to_many 
                and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 
                    'city', 'paid', 'phone', 'created']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['paid']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
admin.site.register(model_or_iterable=Order, admin_class=OrderAdmin)

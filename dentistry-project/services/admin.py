from django.contrib import admin
from .models import Service, Option


class OptionInLine(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = (OptionInLine,)
    list_display = ('name', 'specialization', 'duration',
                    'get_min_price', 'get_max_price')

    @admin.display(description='Минимальная цена')
    def get_min_price(self, obj):
        return format(obj.min_price, ',').replace(',', '.')

    @admin.display(description='Максимальная цена')
    def get_max_price(self, obj):
        return format(obj.max_price, ',').replace(',', '.')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price')
    list_editable = ('price',)

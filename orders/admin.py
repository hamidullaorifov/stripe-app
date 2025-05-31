from django.contrib import admin
from .models import Order, Discount, Tax


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items', 'discount', 'tax', 'get_total_amount')
    filter_horizontal = ('items',)

    def get_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    get_items.short_description = 'Items'

    def get_total_amount(self, obj):
        return obj.get_total_amount()
    get_total_amount.short_description = 'Total Amount'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent_off', 'stripe_id')
    search_fields = ('name', 'stripe_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'inclusive', 'stripe_id')
    search_fields = ('name', 'stripe_id')

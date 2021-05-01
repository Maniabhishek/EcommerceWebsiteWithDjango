from django.contrib import admin

# Register your models here.
from . models import Coupon, Item, OrderItem, Order, BillingAddress, Payment


class OrderAmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)

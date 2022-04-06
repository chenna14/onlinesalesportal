from atexit import register
from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Seller)
admin.site.register(Manager)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)



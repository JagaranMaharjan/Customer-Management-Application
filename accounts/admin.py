from django.contrib import admin
from .models import Customer, Product, Order, Tag

# Register your models here.

# register customer model in admin panel
admin.site.register(Customer)

# register tag model in admin panel
admin.site.register(Tag)

# register order model in admin panel
admin.site.register(Order)

# register product model in admin panel
admin.site.register(Product)

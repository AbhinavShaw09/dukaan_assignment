from django.contrib import admin
from .models import Account, Store, Category, Product, Customer, Order

admin.site.register(Account)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)

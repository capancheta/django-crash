from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity')


admin.site.register(Product,ProductAdmin)

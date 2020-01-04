from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sales)
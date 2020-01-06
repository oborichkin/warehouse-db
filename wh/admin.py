from django.contrib import admin
from .models import *

class ItemInline(admin.TabularInline):
    model = SalesItem

class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
    class Meta:
        model = Transaction

# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(SalesItem)
admin.site.register(Transaction, TransactionAdmin)
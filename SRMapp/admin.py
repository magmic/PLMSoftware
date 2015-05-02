from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Supplier
from .models import Offer
from .models import Order

class OfferAdmin(admin.ModelAdmin):
	list_display = ('product', 'supplier', 'price')

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Order)
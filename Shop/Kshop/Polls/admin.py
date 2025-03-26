from django.contrib import admin
from .models import Product, Cart, CartItem
from django.utils.html import format_html

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_posted', 'price', 'photo')

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
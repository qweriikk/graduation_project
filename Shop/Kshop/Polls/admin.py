from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Cart, CartItem, Order, OrderItem

# --- Продукты ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_posted', 'price')  # image_tag не включён
    list_filter = ('category',)
    search_fields = ('title',)

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.image.url))
    image_tag.short_description = 'Превью'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

# --- Корзина ---
admin.site.register(Cart)
admin.site.register(CartItem)

# --- Заказы ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
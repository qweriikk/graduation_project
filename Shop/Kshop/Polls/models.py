from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2500)
    date_posted = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Сделаем nullable

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')   
    def __str__(self):
        return f"Корзина {self.user.username}" 
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1) 
    def __str__(self):
        return f"{self.quantity} of {self.product.title} in {self.cart.user.username}'s cart"   
    
ORDER_STATUS_CHOICES = [
    ('created', 'Оформлен'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=15)  
    address = models.TextField("Адрес")
    card_number = models.CharField("Номер карты", max_length=19, blank=True)  
    total_price = models.DecimalField("Сумма заказа", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField("Статус", max_length=20, choices=ORDER_STATUS_CHOICES, default='created')  # <-- добавлено

    def __str__(self):
        return f"Заказ #{self.id} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.title}"
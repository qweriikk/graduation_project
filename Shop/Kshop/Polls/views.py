from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from . import forms
from .models import Product, Cart, CartItem
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm
from .models import Product, Favorite
from .models import Category, Product

# from .models import Article
               
def product_description(request):
    return render(request, "Polls/product_description.html")

class ProductListView(ListView):
    model = Product
    template_name = 'Polls/main.html'  
    context_object_name = 'products'
    # ordering = ['-date_posted']
    
class ProductListViewNew(ListView):
    model = Product
    template_name = 'Polls/main.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка аутентификации пользователя и получение элементов корзины
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = CartItem.objects.filter(cart=cart)  # здесь фильтруем по объекту cart
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name="Polls/product_description.html"
    context_object_name = 'product'
    fields = ['title', 'description', 'price','photo']
    
class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'main.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Получаем корзину текущего пользователя
        cart = Cart.objects.get_or_create(user=self.request.user)
        # Возвращаем все элементы корзины
        return CartItem.objects.filter(cart=cart)
    
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        return redirect("main")
    else:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('main') 

def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('main')

def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('main')

def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})    

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return redirect("main")

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
        return redirect("main")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return redirect("main")

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("main")
        return redirect("main")   
    
def enhypen_view(request):
    category = get_object_or_404(Category, name__iexact='enhypen')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/enhypen.html', {'products': products})

def merch_view(request):
    category = get_object_or_404(Category, name__iexact='merch')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/merch.html', {'products': products})

def new_view(request):
    category = get_object_or_404(Category, name__iexact='new')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/new.html', {'products': products})

def straykids_view(request):
    category = get_object_or_404(Category, name__iexact='straykids')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/straykids.html', {'products': products})

def stocks_view(request):
    return render(request, 'Polls/stocks.html')

def seventeen_view(request):
    category = get_object_or_404(Category, name__iexact='seventeen')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/seventeen.html', {'products': products})
    
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Ищем существующий CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        # Новый товар в корзине — сразу ставим quantity=1
        cart_item.quantity = 1
    else:
        # Уже был — просто увеличиваем
        cart_item.quantity += 1
    cart_item.save()

    return redirect('main')


@login_required
def increase_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Если вдруг не было — создаём
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    return redirect('main')


@login_required
def decrease_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('main')


@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('main')


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('main')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('product').all()
    total_price = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order: Order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            # создаём позиции заказа
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            # очищаем корзину
            cart.items.all().delete()
            messages.success(request, "Заказ успешно оформлен!")
            return redirect('payment_success')
    else:
        form = OrderForm()

    return render(request, 'Polls/checkout.html', {
        'cart_items': items,
        'total_price': total_price,
        'form': form,
    })
    
@login_required
def payment_success(request):
    return render(request, 'Polls/payment_success.html')

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def favorites_view(request):
    # Получаем все Favorite-объекты текущего пользователя
    favs = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'Polls/favorites.html', {'favorites': favs})

@login_required
def add_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'main'))

@login_required
def remove_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('favorites')

def category_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, f'Polls/{category_name.lower()}.html', {
        'products': products,
        'category': category,
    })
    
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Polls/my_orders.html', {'orders': orders})    

# def register_view(request):
#     # if request.user.is_authenticated:
#     #     # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
#     #     return redirect('main')  # Замените 'home' на имя вашего представления или URL

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             # Сохраняем нового пользователя
#             print("valid2")
#             # Аутентифицируем нового пользователя и выполняем вход
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 print("valid3")
#                 login(request, user)
#                 # Перенаправляем пользователя на нужную страницу
#                 return redirect('main')  # Замените 'home' на имя вашего представления или URL
#     else:
#         # Если запрос не методом POST, просто отображаем пустую форму регистрации
#         form = UserCreationForm()
#     return render(request, 'Polls/register.html', {'form': form})

from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View
from django.contrib import messages
from .forms import LoginForm, OrderForm
from .models import Product, Cart, CartItem, Order, OrderItem, Favorite, Category


def product_description(request):
    return render(request, "Polls/product_description.html")


class ProductListView(ListView):
    model = Product
    template_name = 'Polls/main.html'
    context_object_name = 'products'


class ProductListViewNew(ListView):
    model = Product
    template_name = 'Polls/main.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = CartItem.objects.filter(cart=cart)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "Polls/product_description.html"
    context_object_name = 'product'
    fields = ['title', 'description', 'price', 'photo']


class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'Polls/cart_detail.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
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
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
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


def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query) if query else []
    return render(request, 'Polls/search_results.html', {'query': query, 'products': products})


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "Polls/register.html", {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
        return render(request, "Polls/register.html", {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "Polls/login.html", {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("main")
        return render(request, "Polls/login.html", {
            'form': form,
            'error': "Неверное имя пользователя или пароль"
        })
    
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

def twice_view(request):
    category = get_object_or_404(Category, name__iexact='twice')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/twice.html', {'products': products})

def aespa_view(request):
    category = get_object_or_404(Category, name__iexact='aespa')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/aespa.html', {'products': products})

def idle_view(request):
    category = get_object_or_404(Category, name__iexact='idle')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/idle.html', {'products': products})

def itzy_view(request):
    category = get_object_or_404(Category, name__iexact='itzy')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/itzy.html', {'products': products})

def bts_view(request):
    category = get_object_or_404(Category, name__iexact='bts')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/bts.html', {'products': products})

def txt_view(request):
    category = get_object_or_404(Category, name__iexact='txt')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/txt.html', {'products': products})

def ateez_view(request):
    category = get_object_or_404(Category, name__iexact='ateez')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/ateez.html', {'products': products})

def blackpink_view(request):
    category = get_object_or_404(Category, name__iexact='blackpink')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/blackpink.html', {'products': products})

def lesserafim_view(request):
    category = get_object_or_404(Category, name__iexact='lesserafim')
    products = Product.objects.filter(category=category)
    return render(request, 'Polls/lesserafim.html', {'products': products})
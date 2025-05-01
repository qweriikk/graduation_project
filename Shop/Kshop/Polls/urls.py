from django.urls import path
from . import views
from .views import ProductDetailView, ProductListView, RegisterView, LoginView, CartDetailView, ProductListViewNew
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', ProductListView.as_view(), name="main"),
    path('', ProductListViewNew.as_view(), name="main"),
    # path('', CartDetailView.as_view(), name="cart-detail"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # path('description', views.product_description, name="product_description"),
    
    # описание продукта
    path('product/<int:pk>/', ProductDetailView.as_view(), name='post-detail'),
    
    # функционал корзины
    path('cart/', views.cart_detail, name='cart_detail'),
    path('product/<int:pk>/add', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    
    path('orders/', views.order_list, name='order_list'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/checkout/success/', views.payment_success, name='payment_success'),
    
    path('add_favorite/<int:product_id>/', views.add_favorite, name='add_to_favorites'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
    
    path('enhypen/', views.enhypen_view, name='enhypen'),
    path('merch.html', views.merch_view, name='merch'),
    path('new/', views.new_view, name='new'),
    path('straykids/', views.straykids_view, name='straykids'),
    path('stocks/', views.stocks_view, name='stocks'),
    path('seventeen/', views.seventeen_view, name='seventeen'),
    
]
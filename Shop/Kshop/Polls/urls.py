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
    
]
from django.urls import path
from . import views
from .views import ProductDetailView, RegisterView, LoginView, CartDetailView, ProductListViewNew
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Путь для главной страницы
    path('', ProductListViewNew.as_view(), name="main"),
    
    path('search/', views.search_results, name='search_results'),
    
    # Путь для регистрации и входа
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Описание продукта
    path('product/<int:pk>/', ProductDetailView.as_view(), name='post-detail'),
    
    # Корзина
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('product/<int:pk>/add', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    
    # Заказы
    path('orders/', views.order_list, name='order_list'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/checkout/success/', views.payment_success, name='payment_success'),
    
    # Избранное
    path('add_favorite/<int:product_id>/', views.add_favorite, name='add_to_favorites'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
    
    path('stocks/', views.stocks_view, name='stocks'),
    
    # Статичные страницы категорий 
    path('merch.html', views.merch_view, name='merch'),
    path('new/', views.new_view, name='new'),
    path('straykids/', views.straykids_view, name='straykids'),
    path('seventeen/', views.seventeen_view, name='seventeen'),
    path('enhypen/', views.enhypen_view, name='enhypen'),
    path('twice/', views.twice_view, name='twice'),
    path('aespa/', views.aespa_view, name='aespa'),
    path('idle/', views.idle_view, name='idle'),
    path('itzy/', views.itzy_view, name='itzy'),
    path('bts/', views.bts_view, name='bts'),
    path('txt/', views.txt_view, name='txt'),
    path('ateez/', views.ateez_view, name='ateez'),
    path('blackpink/', views.blackpink_view, name='blackpink'),
    path('lesserafim/', views.lesserafim_view, name='lesserafim'),
    
    # Динамичные категории
    path('category/<str:category_name>/', views.category_view, name='category_view'),

]

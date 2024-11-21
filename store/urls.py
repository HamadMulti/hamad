from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.CustomLoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('order/place/', views.place_order, name='place_order'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
]
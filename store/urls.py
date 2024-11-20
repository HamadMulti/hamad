from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('order/place/', views.place_order, name='place_order'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
]

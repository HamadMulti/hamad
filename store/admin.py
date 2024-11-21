from django.contrib import admin
from .models import Product, Category, Order, OrderItem


admin.site.register(Category)
admin.site.register(Product)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'total_price', 'created_at')



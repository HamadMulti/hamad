from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, Category, Order, OrderItem, Product
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_products.html', {'category': category, 'products': products})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')
  
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search.html', {'products': products, 'query': query})


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')

    total_price = sum(item.total_price() for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart_items.delete()
    return render(request, 'store/order_success.html', {'order': order})

def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/dashboard.html', {'orders': orders})


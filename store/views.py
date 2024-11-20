from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, Category, Order, OrderItem, Product
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        merge_cart_items(self.request.user,
                         self.request.session.get('session_key'))
        return response


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(
            username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'store/register.html')


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
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product)
    else:
        session_key = request.session.session_key or get_random_string(32)
        request.session['session_key'] = session_key
        cart_item, created = Cart.objects.get_or_create(
            session_key=session_key, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def view_cart(request):
    cart_items = get_cart_items(request)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if request.user.is_authenticated and cart_item.user != request.user:
        return redirect('cart')
    if not request.user.is_authenticated and cart_item.session_key != request.session.get('session_key'):
        return redirect('cart')
    cart_item.delete()
    return redirect('cart')


def get_cart_items(request):
    session_key = request.session.session_key or get_random_string(32)
    request.session['session_key'] = session_key
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(session_key=session_key)
    return cart_items


def merge_cart_items(user, session_key):
    guest_cart_items = Cart.objects.filter(session_key=session_key)
    for item in guest_cart_items:
        cart_item, created = Cart.objects.get_or_create(
            user=user, product=item.product)
        if not created:
            cart_item.quantity += item.quantity
        cart_item.save()
    guest_cart_items.delete()


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

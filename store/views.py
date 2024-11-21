from django.contrib import messages
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
        user = request.user
        cart_item, created = Cart.objects.get_or_create(
            product=product,
            user=user,
            defaults={'quantity': 1},
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key

        cart_item, created = Cart.objects.get_or_create(
            product=product,
            user=None,
            defaults={'quantity': 1},
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    messages.success(request, f'Added {product.title} to the cart.')
    return redirect('home')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(user=None, session_key=session_key)

    total_cost = sum(item.total_price for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })


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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(user=None, session_key=session_key)

    total_cost = sum(item.total_price for item in cart_items)

    if total_cost > 0:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total_cost
        )

        for item in cart_items:
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect('dashboard')

    return redirect('cart')



def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/dashboard.html', {'orders': orders})

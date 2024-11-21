from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, Category, Order, OrderItem, Product
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from decimal import Decimal


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        merge_cart_items(self.request.user,
                         self.request.session.get('session_key'))

        return response


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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

        cart = request.session.get('cart', {})
        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += 1
        else:
            cart[str(product.id)] = {
                'quantity': 1,
                'price': str(product.price),
            }
        request.session['cart'] = cart

    messages.success(request, f'Added {product.title} to the cart.')
    return redirect('home')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_cost = sum(item.total_price for item in cart_items)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        cart_items = request.session.get('cart', {})
        total_cost = Decimal(0)

        cart_items_display = []
        for product_id, item in cart_items.items():
            product = get_object_or_404(Product, id=product_id)
            cart_items_display.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': Decimal(item['price']) * item['quantity'],
            })
            total_cost += Decimal(item['price']) * item['quantity']

    return render(request, 'store/cart.html', {
        'cart_items': cart_items_display if not request.user.is_authenticated else cart_items,
        'total_cost': total_cost,
    })


def remove_from_cart(request, cart_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return redirect('view_cart')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        try:
            cart_item = Cart.objects.get(id=cart_id, session_key=session_key)
        except Cart.DoesNotExist:
            return redirect('view_cart')
    cart_item.delete()
    return redirect('view_cart')


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
            user=user, product=item.product
        )
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
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    if not cart or not cart.items.exists():
        return redirect('view_cart')  # Redirect if the cart is empty

    total_cost = sum(item.total_price for item in cart.items.all())

    if total_cost > 0:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total_cost
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                image=item.product.image if hasattr(
                    item.product, 'image') else None
            )

        cart.items.all().delete()

        return redirect('dashboard')

    return redirect('view_cart')


def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/dashboard.html', {'orders': orders})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product  # Assuming you have a Product model
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'store/product_list.html', {'products': products,'cart_count': cart_count,})

class CustomLoginView(LoginView):
    template_name = 'store/login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically logs in the new user
            messages.success(request, f"Welcome {user.username},your account was created successfully!")
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # Add product or increment quantity
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('product_list')

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def checkout_view(request):
    # This is a placeholder checkout process
    request.session['cart'] = {}  # Clear the cart
    messages.success(request, "Thank you for your purchase!")
    return redirect('product_list')

@login_required
def increment_quantity(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def decrement_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if cart.get(str(product_id), 0) > 1:
        cart[str(product_id)] -= 1
    else:
        cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
    return {'cart_item_count': sum(cart.values())}
       
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


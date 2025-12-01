from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Producer, Customer, Order
from .forms import ProductForm, ProducerForm, CustomerRegistrationForm, CustomerUpdateForm

# MAIN PAGES
def landing_page(request):
    featured_products = Product.objects.all()[:6]
    producers_count = Producer.objects.count()
    products_count = Product.objects.count()
    
    context = {
        'featured_products': featured_products,
        'producers_count': producers_count,
        'products_count': products_count,
    }
    return render(request, 'Tconnect/landing.html', context)

def products_list(request):
    products = Product.objects.all()
    return render(request, 'Tconnect/products_list.html', {'products': products})

def producers_list(request):
    producers = Producer.objects.all()
    return render(request, 'Tconnect/producers_list.html', {'producers': producers})

# PRODUCT CRUD
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()
    
    return render(request, 'Tconnect/product_form.html', {
        'form': form,
        'title': 'Add New Product'
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Tconnect/product_detail.html', {
        'product': product
    })

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'Tconnect/product_form.html', {
        'form': form,
        'title': f'Edit {product.name}',
        'product': product
    })

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products_list')
    
    return render(request, 'Tconnect/product_confirm_delete.html', {
        'product': product
    })

# PRODUCER CRUD
def producer_create(request):
    if request.method == 'POST':
        form = ProducerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producers_list')
    else:
        form = ProducerForm()
    
    return render(request, 'Tconnect/producer_form.html', {
        'form': form,
        'title': 'Add New Producer'
    })

def producer_detail(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    products = producer.products.all()
    return render(request, 'Tconnect/producer_detail.html', {
        'producer': producer,
        'products': products
    })

def producer_update(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    
    if request.method == 'POST':
        form = ProducerForm(request.POST, instance=producer)
        if form.is_valid():
            form.save()
            return redirect('producers_list')
    else:
        form = ProducerForm(instance=producer)
    
    return render(request, 'Tconnect/producer_form.html', {
        'form': form,
        'title': f'Edit {producer.name}',
        'producer': producer
    })

def producer_delete(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    
    if request.method == 'POST':
        producer.delete()
        return redirect('producers_list')
    
    return render(request, 'Tconnect/producer_confirm_delete.html', {
        'producer': producer
    })

# AUTHENTICATION
def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to TailorConnect.')
            return redirect('landing')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'Tconnect/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('landing')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'Tconnect/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')

@login_required
def profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            contact_info='',
            location=''
        )
    
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerUpdateForm(instance=customer)
    
    orders = Order.objects.filter(customer=customer)
    
    return render(request, 'Tconnect/profile.html', {
        'form': form,
        'customer': customer,
        'orders': orders
    })

# ORDER MANAGEMENT
@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        total_price = product.price * quantity
        
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                user=request.user,
                contact_info='',
                location=''
            )
        
        order = Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        
        messages.success(request, f'Order placed successfully! Order #{order.id}')
        return redirect('order_detail', pk=order.pk)
    
    return render(request, 'Tconnect/create_order.html', {
        'product': product
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Ensure the user can only see their own orders
    if order.customer.user != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('landing')
    
    return render(request, 'Tconnect/order_detail.html', {
        'order': order
    })

@login_required
def order_list(request):
    try:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer).order_by('-order_date')
    except Customer.DoesNotExist:
        orders = []
    
    return render(request, 'Tconnect/order_list.html', {
        'orders': orders
    })
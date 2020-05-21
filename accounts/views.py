from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import *
from .forms import orderForm, CreateUserForm, CustomerForm
from .filters import orderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password')

    context = {
            }
    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register_page(request):
    
    register_form = CreateUserForm()

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            username = register_form.cleaned_data.get('username')          

            messages.success(request, 'User ' + username + ' created successfully')
            return redirect('login')

    context = {
        'register_form': register_form,
    }
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    orders_total = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'orders_total': orders_total,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }

    return render(request, 'accounts/main.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    orders_total = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    order_filter = orderFilter(request.GET, queryset=orders)
    orders = order_filter.qs
    
    context = {
        'orders': orders,
        'order_filter': order_filter,
        'orders_total': orders_total,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):

    customer = request.user.customer
    customer_form = CustomerForm(instance=customer)
        
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        if customer_form.is_valid():
            customer_form.save()
            #return redirect('account_settings')

    context = {
        'customer_form': customer_form,
    }
    return render(request, 'accounts/account.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_orders = customer.order_set.all()
    customer_total_orders = customer_orders.count()

    order_filter = orderFilter(request.GET, queryset=customer_orders)
    customer_orders = order_filter.qs

    context = {
        'customer': customer,
        'customer_orders': customer_orders,
        'customer_total_orders': customer_total_orders,
        'order_filter': order_filter,
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    
    OrderInlineFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    formset = OrderInlineFormSet()
    #form = orderForm(initial = {'customer': customer})

    if request.method == 'POST':
        #print('new order created')
        formset = OrderInlineFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)

    if request.method == 'POST':
        form  = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'order': order,
    }

    return render(request, 'accounts/delete_form.html', context)

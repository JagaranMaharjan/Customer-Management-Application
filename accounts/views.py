from django.shortcuts import render, redirect
from django.http import HttpResponse

from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.

# register
@unauthenticated_user
def registerPage(request):
    # form = UserCreationForm() --- replace by create user form
    form = CreateUserForm()
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # get username from form and hold that username
            username = form.cleaned_data.get('username')
            # set default group of new users to customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # set one to one relationship
            Customer.objects.create(user=user)
            # display message of new user registration successful
            messages.success(request, 'Account was created for ' + username)
            # redirect to login page after successful registration
            return redirect('login')
    # created dictionary to display data in template
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# user login
@unauthenticated_user
def loginPage(request):
    # if request method is post then
    if request.method == 'POST':
        # hold username
        username = request.POST.get('username')
        # hold password
        password = request.POST.get('password')
        # check user is valid or not
        user = authenticate(request, username=username, password=password)
        # if username or password is valid then
        if user is not None:
            # redirect to dashboard
            login(request, user)
            return redirect('home')
        else:
            # if not valid then display error message
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


# logout
def logoutUser(request):
    # clear all session and cookies
    logout(request)
    # redirect to login page
    return redirect('login')


# display dashboard
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    # return all orders from order table
    orders = Order.objects.all()
    # return all customers from customer table
    customers = Customer.objects.all()
    # count total customers
    total_customers = customers.count()
    # count total orders
    total_orders = orders.count()
    # count total product delivered
    total_delivered = orders.filter(status='Delivered').count()
    # count total pending product to be delivered
    total_pending = orders.filter(status='Pending').count()
    # created dictionary to pass value in template
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'total_delivered': total_delivered, 'total_pending': total_pending}
    return render(request, 'accounts/dashboard.html', context)


# customer user page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    # get all orders of customer by pk
    orders = request.user.customer.order_set.all()
    # count total orders
    total_orders = orders.count()
    # count total product delivered
    total_delivered = orders.filter(status='Delivered').count()
    # count total pending product to be delivered
    total_pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_orders': total_orders, 'total_delivered': total_delivered,
               'total_pending': total_pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


# display product ui
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    # return all products from product table
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


# display customer ui
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    # return customer details according to customer id
    customer = Customer.objects.get(id=pk_test)
    # Returns all orders related to customer
    orders = customer.order_set.all()
    # return total orders
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    # created dictionary to pass value in template
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


# create order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=['product', 'status'], extra=5)
    customer = Customer.objects.get(id=pk)
    # formset = OrderFormSet(instance=customer)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # return all orders from order table according customer id
    # form = OrderForm(initial={'customer': customer})
    # if form method is post then
    if request.method == 'POST':
        # print('Printing Post: ', request.POST)
        # hold user input new form data
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        # if user input new form data is valid then
        # if form.is_valid():
        if formset.is_valid():
            # save those data on database
            # form.save()
            formset.save()
            # and redirect into dashboard
            return redirect('/')
    # created dictionary to display value in template
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


# update order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def updateOrder(request, pk):
    # return order details according to order id
    order = Order.objects.get(id=pk)
    # hold data in form according to order id
    form = OrderForm(instance=order)
    # if form method is post then
    if request.method == 'POST':
        # if user has updated form data then hold it
        form = OrderForm(request.POST, instance=order)
        # if user updated new form data is valid then
        if form.is_valid():
            # save and update those data in database according to order id
            form.save()
            # and redirect to dashboard
            return redirect('/')
    # created dictionary to display value in template
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


# delete order for forever
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, pk):
    # return order details according to order id
    order = Order.objects.get(id=pk)
    # if form method is post then
    if request.method == 'POST':
        # if user confirm data to be delete then delete selected data from database
        order.delete()
        # and redirect to dashboard
        return redirect('/')
    # created dictionary to display value in template
    context = {'order': order}
    return render(request, 'accounts/delete.html', context)

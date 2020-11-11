from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import OrderFilter


# Create your views here.
# display dashboard
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


# display product ui
def products(request):
    # return all products from product table
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


# display customer ui
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

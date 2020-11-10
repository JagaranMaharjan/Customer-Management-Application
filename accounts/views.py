from django.shortcuts import render
from django.http import HttpResponse
from .models import *


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
    # created dictionary to pass value in template
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)

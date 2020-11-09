from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# display dashboard
def home(request):
    return render(request, 'accounts/dashboard.html')


# display product ui
def products(request):
    return render(request, 'accounts/products.html')


# display customer ui
def customer(request):
    return render(request, 'accounts/customer.html')

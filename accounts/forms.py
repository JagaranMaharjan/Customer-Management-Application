from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# created order form

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


# product order form for customer
class OrderForm(ModelForm):
    class Meta:
        # referenced of order model
        model = Order
        # all order model attributes are required
        fields = '__all__'


# user creation form
class CreateUserForm(UserCreationForm):
    class Meta:
        # referenced of user model
        model = User
        # made custom field
        fields = ['username', 'email', 'password1', 'password2']

from django.forms import ModelForm
from .models import Order


# created order form

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

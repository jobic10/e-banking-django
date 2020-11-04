import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from .forms import *
from .models import *

# Create your views here.


def generate_account_number(account_type):
    number = ''.join(random.choices(string.digits, k=10))
    if Customer.objects.filter(account_number=number, account_type=account_type).exists():
        return generate_account_number()
    return number


def generate_pin_number():
    number = ''.join(random.choices(string.digits, k=4))
    return number


def create_customer_account(request):
    userForm = UserForm(request.POST or None, request.FILES or None)
    customerForm = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if all([userForm.is_valid(), customerForm.is_valid()]):
            user = userForm.save(commit=False)
            user.user_type = 3
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            account_number = generate_account_number(customer.account_type)
            pin = generate_pin_number()
            customer.account_number = account_number
            customer.pin = pin
            customer.save()
            messages.success(
                request, f"Dear Customer, Your Account Number is {account_number}. \nWelcome to Corona Bank ")
            return redirect(reverse('view_customer', args=[customer.id]))
        else:
            messages.error(
                request, f"Form Errors: \n {customerForm.errors} \n {userForm.errors}   ")
    context = {'user_form': userForm, 'customer_form': customerForm}
    return render(request, "account/customer_form.html", context)


def view_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    context = {'customer': customer}
    return render(request, "account/view_customer.html", context)

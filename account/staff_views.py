from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def create_customer_account(request):
    userForm = UserForm()
    customerForm = CustomerForm()
    context = {'user_form': userForm, 'customer_form': customerForm}
    return render(request, "account/form.html", context)

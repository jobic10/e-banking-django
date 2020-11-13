import random
import string
from transaction.views import credit_transaction
from transaction.models import Transaction
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .filters import *
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
    from random import randint
    total = 5
    x = randint(2, 3)
    y = 5 - x
    customer = get_object_or_404(Customer, id=customer_id)
    credit_transactions = Transaction.objects.filter(
        receiver=customer.user, status=1).only('amount', 'updated_at', 'description')
    debit_transactions = Transaction.objects.filter(
        sender=customer.user, status=1).only('amount', 'updated_at', 'description')
    if len(credit_transactions) > x:
        credit_transactions = credit_transactions[:x]
    if len(debit_transactions) > y:
        debit_transactions = debit_transactions[:y]

    context = {'customer': customer,
               'credit_transactions': credit_transactions,
               'debit_transactions': debit_transactions
               }
    return render(request, "account/view_customer.html", context)


def manage_all_customer(request):
    allCustomers = Customer.objects.all()
    paginator = Paginator(allCustomers, 25)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    context = {
        'customers': customers
    }
    return render(request, "account/manage_customer.html", context)


def manage_savings_customer(request):
    allCustomers = Customer.objects.filter(account_type='Savings')
    paginator = Paginator(allCustomers, 25)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    context = {
        'customers': customers
    }
    return render(request, "account/manage_customer.html", context)


def manage_current_customer(request):
    allCustomers = Customer.objects.filter(account_type='current')
    paginator = Paginator(allCustomers, 25)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    context = {
        'customers': customers
    }
    return render(request, "account/manage_customer.html", context)


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    userForm = UserEditForm(request.POST or None,
                            request.FILES or None, instance=customer.user)
    customerForm = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST':
        if all([userForm.is_valid(), customerForm.is_valid()]):
            userForm.save()
            customerForm.save()
            messages.success(
                request, f"Customer Detail Updated")
            return redirect(reverse('view_customer', args=[customer.id]))
        else:
            messages.error(
                request, f"Form Errors: \n {customerForm.errors} \n {userForm.errors}   ")
    context = {'user_form': userForm,
               'customer_form': customerForm, 'isEdit': True}
    return render(request, "account/customer_form.html", context)


def search_customer(request):
    allCustomers = Customer.objects.all()
    filter = CustomerFilter(request.GET, queryset=allCustomers)
    customers = filter.qs
    context = {
        'filter': filter,
        'customers': customers
    }
    return render(request, "account/search.html", context)

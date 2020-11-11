from django.shortcuts import get_object_or_404, render
from account.models import *
# Create your views here.


def start_transaction(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return customer


def credit_transaction(request):
    pass


def debit_transaction(request):
    pass


def transaction_logs(request):
    pass

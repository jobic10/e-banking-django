from django.shortcuts import get_object_or_404, render
from account.models import *
from django.contrib import messages
from .forms import CreditForm
# Create your views here.


def credit_transaction(request):
    form = CreditForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            pass
        else:
            messages.error(request, "Form invalid!")
    return render(request, "account/credit.html", context)


def debit_transaction(request):
    context = {}
    return render(request, "account/customer_form.html", context)


def transaction_logs(request):
    context = {}
    return render(request, "account/customer_form.html", context)

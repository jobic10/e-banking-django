from transaction.models import BankCreditTransaction
from django.shortcuts import get_object_or_404, render, reverse, redirect
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
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Transaction Started. Please Verify.")
            return redirect(reverse('verify_transaction', args=[obj.id]))
        else:
            messages.error(request, "Form invalid!")
    return render(request, "account/credit.html", context)


def debit_transaction(request):
    context = {}
    return render(request, "account/customer_form.html", context)


def transaction_logs(request):
    context = {}
    return render(request, "account/customer_form.html", context)


def verify_transaction(request, transaction_id):
    transaction = get_object_or_404(BankCreditTransaction, id=transaction_id)
    if transaction.status != 0:
        messages.error(request, "Sorry, this transaction has expired!")
        return redirect(reverse('dashboard'))
    else:
        context = {
            'transaction': transaction
        }
        if request.method == 'POST':
            if request.POST.get('approve') == None:  # Transaction was not approved
                transaction.status = -1
                transaction.save()
                messages.info(request, "Transaction has been cancelled.")
                return redirect(reverse('dashboard'))
            else:  # Approved Transaction
                customer = transaction.customer
                customer.balance += transaction.amount
                transaction.balance_before = customer.balance
                transaction.status = 1
                customer.save()
                transaction.save()
                messages.success(request, "Transaction has been approved.")
                return redirect(reverse('dashboard'))

        return render(request, "account/verify.html", context)

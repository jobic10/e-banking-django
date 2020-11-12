from transaction.models import Transaction
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
            obj.sender = request.user
            obj.save()
            id = obj.id
            messages.success(
                request, f"Transaction Started. Please Confirm Transaction#{id}.")
            return redirect(reverse('verify_transaction', args=[id]))
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
    transaction = get_object_or_404(Transaction, id=transaction_id)
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
                try:
                    customer = transaction.receiver.customer  # Get balance
                    transaction.balance_before = customer.balance
                    customer.balance += transaction.amount
                    transaction.status = 1
                    customer.save()
                    transaction.save()
                    messages.success(
                        request, "Transaction has been approved.")
                    return redirect(reverse('view_customer', args=[customer.id]))
                except:
                    messages.error(request, "Transaction Error.")

        return render(request, "account/verify.html", context)

from transaction.models import Transaction
from django.shortcuts import get_object_or_404, render, reverse, redirect
from account.models import *
from django.db.models import Q
from django.contrib import messages
from .forms import CreditForm
from django.core.paginator import Paginator
# Create your views here.


def credit_transaction(request):
    form = CreditForm(request.POST or None, form_type="C")
    context = {
        'form': form,
        'type': 'Credit'
    }
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = request.user
            obj.category = 'C'
            obj.save()
            id = obj.id
            messages.success(
                request, f"Transaction Started. Please Confirm Transaction #{id}.")
            return redirect(reverse('verify_transaction', args=[id]))
        else:
            messages.error(request, "Form invalid!")
    return render(request, "account/start_transaction.html", context)


def debit_transaction(request):
    #! Remember this
    if request.user.is_staff:  # Bank Debit
        pass  # Bank
    else:
        pass  # Customer
    form = CreditForm(request.POST or None, form_type="D")
    context = {
        'form': form,
        'type': 'Debit'
    }
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.receiver = request.user
            obj.category = 'D'
            obj.save()
            id = obj.id
            messages.success(
                request, f"Transaction Started. Please Confirm Transaction #{id}.")
            return redirect(reverse('verify_transaction', args=[id]))
        else:
            messages.error(request, "Form invalid!")
    return render(request, "account/start_transaction.html", context)


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
                    if transaction.category == 'D':
                        # Debit
                        customer = transaction.sender.customer  # Get balance
                        transaction.balance_before = customer.balance
                        customer.balance -= transaction.amount
                    else:
                        # Credit
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
                    messages.error(request, "Transaction Error")

        return render(request, "account/verify.html", context)


def view_transaction(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    querySet = Transaction.objects.filter(Q(receiver=customer.user) | Q(
        sender=customer.user), status=1).values('amount', 'updated_at', 'description', 'category')
    paginator = Paginator(querySet, 25)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    context = {'customer': customer,
               'transactions': transactions,
               }
    return render(request, "account/view_transactions.html", context)

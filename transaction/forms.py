from .models import Transaction
from django import forms
from account.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q
# Create your models here.


class CreditForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[(None, '----'), ('Savings', 'Savings'), ('Current', 'Current')])
    sender = forms.CharField(max_length=15, label="Account Number")
    receiver = forms.CharField(max_length=15, label="Account Number")
    balance_before = None

    def __init__(self, *args, **kwargs):
        self.form_type = kwargs.pop('form_type', None)
        self.staff = kwargs.pop('staff', None)
        super(CreditForm, self).__init__(*args, **kwargs)
        if self.form_type == 'C':
            self.type = "credit"
            del self.fields['sender']
        else:
            self.type = "debit"
            del self.fields['receiver']
        self.fields['amount'] = forms.FloatField(
            label=f"Amount to be {self.type}ed")
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean_receiver(self):
        if self.form_type != 'C' or self.staff:  # This is Debit
            return
        cleaned_data = super().clean()
        account_number = cleaned_data.get('receiver')
        account_type = self.data.get('account_type')
        try:
            customer = Customer.objects.get(
                account_number=account_number, account_type=account_type)
            return customer.user
        except:
            suggested_account = Customer.objects.filter(
                Q(account_number__startswith=account_number) | Q(account_number__endswith=account_number))
            if suggested_account.exists():
                first_suggested_account = suggested_account[0]
                if first_suggested_account.account_type != account_type:
                    msg = f"Perhaps... You selected the wrong account type"
                else:
                    msg = f"Did you mean {first_suggested_account.account_number} with account type {first_suggested_account.account_type}"
                raise ValidationError(
                    _(f'No matching account number with the selected account type. {msg}?'))
            raise ValidationError(
                _('Invalid Account Number Specified'),
                _('Account Number Error')
            )

    def clean_sender(self):
        if self.form_type != 'D':  # This is Credit
            return
        cleaned_data = super().clean()
        account_number = cleaned_data.get('sender')
        account_type = self.data.get('account_type')
        try:
            customer = Customer.objects.get(
                account_number=account_number, account_type=account_type)
            return customer.user
        except:
            suggested_account = Customer.objects.filter(
                Q(account_number__startswith=account_number) | Q(account_number__endswith=account_number))
            if suggested_account.exists():
                first_suggested_account = suggested_account[0]
                if first_suggested_account.account_type != account_type:
                    msg = f"Perhaps... You selected the wrong account type"
                else:
                    msg = f"Did you mean {first_suggested_account.account_number} with account type {first_suggested_account.account_type}"
                raise ValidationError(
                    _(f'No matching account number with the selected account type. {msg}?'))
            raise ValidationError(
                _('Invalid Account Number Specified'),
                _('Account Number Error')
            )

    def clean_amount(self):
        if self.form_type != 'D':
            return
        cleaned_data = super().clean()
        # Current can withdraw all money, Savings must have least  #500; so we check to see that this is enforced
        amount = cleaned_data.get('amount')
        user = cleaned_data.get('sender')
        if user != None:
            customer = user.customer
            if customer is not None:
                acct_type = customer.account_type
                balance = customer.balance
                if (balance - amount) < 1:
                    raise ValidationError(
                        _("After withdrawal, account balance is less than zero"), _("Invalid Amount! "))
                if acct_type == 'Savings' and (balance - amount) < 500:
                    raise ValidationError(
                        _("Account type is 'Savings'. After withdrawal, account balance is less than #500"), _("Invalid Amount! "))
        return amount

    class Meta:
        model = Transaction
        fields = ['receiver', 'sender', 'account_type',
                  'amount', 'description']


class TransferForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[(None, '----'), ('Savings', 'Savings'), ('Current', 'Current')])
    sender = forms.CharField(max_length=15, label="Account Number")
    receiver = forms.CharField(max_length=15, label="Account Number")
    balance_before = None

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        self.form_type = kwargs.pop('form_type', None)
        self.staff = kwargs.pop('staff', None)
        super(TransferForm, self).__init__(*args, **kwargs)
        del self.fields['sender']
        self.fields['amount'] = forms.FloatField(
            label=f"Amount to be transferred")
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean_receiver(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get('receiver')
        account_type = self.data.get('account_type')
        try:
            customer = Customer.objects.get(
                account_number=account_number, account_type=account_type)
            if customer == self.creator.customer:
                raise ValueError
            return customer.user
        except ValueError:
            raise ValidationError(
                _('You cannot transfer from your account to your account'), _('Invalid Account'))
        except:
            suggested_account = Customer.objects.filter(
                Q(account_number__startswith=account_number) | Q(account_number__endswith=account_number))
            if suggested_account.exists():
                first_suggested_account = suggested_account[0]
                if first_suggested_account.account_type != account_type:
                    msg = f"Perhaps... You selected the wrong account type"
                else:
                    msg = f"Did you mean {first_suggested_account.account_number} with account type {first_suggested_account.account_type}"
                raise ValidationError(
                    _(f'No matching account number with the selected account type. {msg}?'))
            raise ValidationError(
                _('Invalid Account Number Specified'),
                _('Account Number Error')
            )

    def clean_amount(self):
        cleaned_data = super().clean()
        # Current can withdraw all money, Savings must have least  #500; so we check to see that this is enforced
        amount = cleaned_data.get('amount')
        user = cleaned_data.get('sender')
        if user != None:
            customer = user.customer
            if customer is not None:
                acct_type = customer.account_type
                balance = customer.balance
                if (balance - amount) < 1:
                    raise ValidationError(
                        _("After withdrawal, account balance is less than zero"), _("Invalid Amount! "))
                if acct_type == 'Savings' and (balance - amount) < 500:
                    raise ValidationError(
                        _("Account type is 'Savings'. After withdrawal, account balance is less than #500"), _("Invalid Amount! "))
        return amount

    class Meta:
        model = Transaction
        fields = ['receiver', 'sender', 'account_type',
                  'amount', 'description']

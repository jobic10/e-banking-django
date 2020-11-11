from .models import Transaction
from django import forms
from account.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q
# Create your models here.


class CreditForm(forms.Form):
    account_type = forms.ChoiceField(
        choices=[(None, '----'), ('Savings', 'Savings'), ('Current', 'Current')])
    account_number = forms.CharField(max_length=15)
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(CreditForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean_account_number(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get('account_number')
        account_type = cleaned_data.get('account_type')
        try:
            Customer.objects.get(
                account_number=account_number, account_type=account_type)
            return account_number
        except:
            suggested_account = Customer.objects.filter(
                Q(account_number__startswith=account_number) | Q(account_number__endswith=account_number))
            if suggested_account.exists():
                first_suggested_account = suggested_account[0]
                if first_suggested_account.account_type != account_type:
                    msg = f"Perhaps... You selected the wrong account type "
                else:
                    msg = f"Did you mean {first_suggested_account.account_number} with account type {first_suggested_account.account_type}"
                raise ValidationError(
                    _(f'Invalid Account, {msg}?'))
            raise ValidationError(
                _('Invalid Account Number Specified'),
                _('Account Number Error')
            )

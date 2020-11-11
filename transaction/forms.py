from .models import Transaction
from django import forms
from account.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
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
        try:
            account_number = cleaned_data.get('account_number')
            account_type = cleaned_data.get('account_type')
            Customer.objects.get(
                account_number=account_number, account_type=account_type)
            return account_number
        except:
            raise ValidationError(
                _('Invalid Account Number Specified'),
                _('Account Number Error')
            )

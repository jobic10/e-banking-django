from django import forms
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomerForm(FormSettings):
    class Meta:
        model = Customer
        fields = ('account_type', 'account_number', 'pin',
                  'date_of_birth', 'balance', 'phone', )


class UserForm(FormSettings):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',
                  'user_type', 'gender', 'profile_pic', 'address', )

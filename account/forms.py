from django import forms
from django.forms.widgets import DateInput
from .models import *
from django.contrib.auth.forms import UserCreationForm


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomerForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['balance'].disabled = True

    class Meta:
        model = Customer
        fields = ('phone', 'date_of_birth', 'account_type',
                  'balance', )
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }


class UserForm(UserCreationForm, FormSettings):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',
                  'gender', 'profile_pic', 'address')


class UserEditForm(FormSettings):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',
                  'gender', 'profile_pic', 'address')

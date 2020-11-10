from .models import *
import django_filters
from django import forms
from django_filters import DateFilter, CharFilter


class CustomerFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(CustomerFilter, self).__init__(*args, **kwargs)

        for field in self.filters:
            self.filters[field].field.widget.attrs.update(
                {'class': 'form-control'})

    last_name = CharFilter(field_name='user__last_name',
                           lookup_expr='icontains')
    first_name = CharFilter(
        field_name='user__first_name', lookup_expr='icontains')
    email = CharFilter(field_name='user__email', lookup_expr='icontains')
    date_of_birth = DateFilter(field_name='date_of_birth', lookup_expr='exact',
                               widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Customer
        fields = ('account_type', 'account_number', 'phone', )

from django.db import models
from account.models import Customer
# Create your models here.


class Debit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    description = models.CharField(max_length=100)
    balance_before = models.FloatField()
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    TYPE = [('Debit', 'Debit'), ('Credit', 'Credit')]
    receiver = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    sender = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    description = models.CharField(max_length=100)
    balance_before = models.FloatField()
    amount = models.FloatField()
    category = models.CharField(max_length=5, choices=TYPE)
    created_at = models.DateTimeField(auto_now=True)

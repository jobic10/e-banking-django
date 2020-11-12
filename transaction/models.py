from django.db import models
from account.models import Customer
# Create your models here.


class Transaction(models.Model):
    TYPE = [('Debit', 'Debit'), ('Credit', 'Credit')]
    sender = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="receiver")
    description = models.CharField(max_length=100)
    balance_before = models.FloatField()
    amount = models.FloatField()
    status = models.SmallIntegerField(
        default=0, help_text="If 0, transaction is pending; approved if 1, rejected if -1")
    category = models.CharField(max_length=6, choices=TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

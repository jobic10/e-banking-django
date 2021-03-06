from django.db import models
from account.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Transaction(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver")
    description = models.CharField(max_length=100)
    balance_before = models.FloatField(null=True, blank=True)
    amount = models.FloatField(validators=[
        MinValueValidator(10)
    ])
    category = models.CharField(max_length=6, choices=[
                                ('C', 'Credit'), ('D', 'Debit'), ('T', 'Transfer')])
    status = models.SmallIntegerField(
        default=0, help_text="If 0, transaction is pending; approved if 1, rejected if -1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

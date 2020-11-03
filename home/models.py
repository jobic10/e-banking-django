from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField(verbose_name="How can we help ")
    reply = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

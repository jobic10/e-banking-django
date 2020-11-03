from django.db import models

# Create your models here.


class Advert(models.Model):
    subject = models.CharField(max_length=20)
    note = models.TextField(verbose_name="Advert Note")
    img = models.ImageField(null=True, upload_to='advert')
    url = models.URLField(null=True)
    CHOICE = [(1, 'Active'), (0, 'Inactive')]
    status = models.SmallIntegerField(default=1, choices=CHOICE)

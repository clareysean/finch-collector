from django.db import models


class Finch(models.Model):
    name = models.CharField(max_length=100)
    threats = models.TextField(max_length=250)
    habitat = models.CharField(max_length=100)
    notes = models.TextField(max_length=250)

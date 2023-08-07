from django.db import models
from django.urls import reverse


class Finch(models.Model):
    name = models.CharField(max_length=100)
    threats = models.TextField(max_length=250)
    habitat = models.CharField(max_length=100)
    notes = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

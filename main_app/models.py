from django.db import models
from django.urls import reverse
# from datetime import date

TIME_OF_DAY = (('M', 'Morning'), ('A', 'Afternoon'),
               ('E', 'Evening'), ('N', 'Night'))


class Finch(models.Model):
    name = models.CharField(max_length=100)
    threats = models.TextField(max_length=250)
    habitat = models.CharField(max_length=100)
    notes = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})


class Sighting(models.Model):
    date = models.DateField('Sighting date')
    tod = models.CharField(
        max_length=1,
        choices=TIME_OF_DAY,
        default=TIME_OF_DAY[0][0]
    )

    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_tod_display()} on {self.date}"

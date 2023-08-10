from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


TIME_OF_DAY = (('M', 'Morning'), ('A', 'Afternoon'),
               ('E', 'Evening'), ('N', 'Night'))


class Food(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('foods_detail', kwargs={'pk': self.id})


class Finch(models.Model):
    name = models.CharField(max_length=100)
    threats = models.TextField(max_length=250)
    habitat = models.CharField(max_length=100)
    notes = models.TextField(max_length=250)

    foods = models.ManyToManyField(Food)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for finch_id: {self.finch_id} @{self.url}"


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

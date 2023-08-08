from django.forms import ModelForm
from .models import Sighting


class SightingForm(ModelForm):
    class Meta:
        model = Sighting
        fields = ['date', 'tod']
        labels = {
            'date': 'Sighting Date',
            'tod': 'Time of Day'
        }

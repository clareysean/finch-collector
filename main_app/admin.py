from django.contrib import admin
from .models import Finch, Sighting, Food, Photo

admin.site.register(Finch)
admin.site.register(Sighting)
admin.site.register(Food)
admin.site.register(Photo)

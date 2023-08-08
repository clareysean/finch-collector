from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
from .forms import SightingForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    sighting_form = SightingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'sighting_form': sighting_form
    })

# def cats_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id)
#     feeding_form = FeedingForm()
#     return render(request, 'cats/detail.html', {
#         'cat': cat,
#         'feeding_form': feeding_form
#     })


def add_sighting(request, finch_id):
    # create a ModelForm instance using the data in request.POST
    form = SightingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_sighting = form.save(commit=False)
        new_sighting.finch_id = finch_id
        new_sighting.save()
    return redirect('detail', finch_id=finch_id)


class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'


class FinchUpdate(UpdateView):
    model = Finch
    fields = ['habitat', 'notes', 'threats']


class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Food, Photo
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
    id_list = finch.foods.all().values_list('id')
    foods_finch_doesnt_have = Food.objects.exclude(id__in=id_list)

    sighting_form = SightingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'sighting_form': sighting_form,
        'foods': foods_finch_doesnt_have
    })


def add_sighting(request, finch_id):
    # create a ModelForm instance using the data in request.POST
    form = SightingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the finch_id assigned
        new_sighting = form.save(commit=False)
        new_sighting.finch_id = finch_id
        new_sighting.save()
    return redirect('detail', finch_id=finch_id)


def add_photo(request, finch_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, finch_id=finch_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', finch_id=finch_id)


class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'threats', 'habitat', 'notes']


class FinchUpdate(UpdateView):
    model = Finch
    fields = ['habitat', 'notes', 'threats']


class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'


class FoodList(ListView):
    model = Food


class FoodDetail(DetailView):
    model = Food


class FoodCreate(CreateView):
    model = Food
    fields = '__all__'


class FoodUpdate(UpdateView):
    model = Food
    fields = ['name', 'details']


class FoodDelete(DeleteView):
    model = Food
    success_url = '/foods'


def assoc_food(request, finch_id, food_id):
    Finch.objects.get(id=finch_id).foods.add(food_id)
    return redirect('detail', finch_id=finch_id)


def unassoc_food(request, finch_id, food_id):
    Finch.objects.get(id=finch_id).foods.remove(food_id)
    return redirect('detail', finch_id=finch_id)

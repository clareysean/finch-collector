import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Food, Photo
from .forms import SightingForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches': finches})


@login_required
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


@login_required
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


@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'threats', 'habitat', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['habitat', 'notes', 'threats']


class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches'


class FoodList(LoginRequiredMixin, ListView):
    model = Food


class FoodDetail(LoginRequiredMixin, DetailView):
    model = Food


class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food
    fields = '__all__'


class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    fields = ['name', 'details']


class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = '/foods'


@login_required
def assoc_food(request, finch_id, food_id):
    Finch.objects.get(id=finch_id).foods.add(food_id)
    return redirect('detail', finch_id=finch_id)


@login_required
def unassoc_food(request, finch_id, food_id):
    Finch.objects.get(id=finch_id).foods.remove(food_id)
    return redirect('detail', finch_id=finch_id)

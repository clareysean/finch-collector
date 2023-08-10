from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('finches/', views.finches_index, name='index'),
    path('finches/<int:finch_id>', views.finches_detail, name='detail'),
    path('finches/create/', views.FinchCreate.as_view(), name='finches_create'),
    path('finches/<int:pk>/update/',
         views.FinchUpdate.as_view(), name='finches_update'),
    path('finches/<int:pk>/delete/',
         views.FinchDelete.as_view(), name='finches_delete'),
    path('finches/<int:finch_id>/add_sighting/',
         views.add_sighting, name='add_sighting'),
    path('finches/<int:finch_id>/assoc_food/<int:food_id>/',
         views.assoc_food, name='assoc_food'),
    path('finches/<int:finch_id>/unassoc_food/<int:food_id>/',
         views.unassoc_food, name='unassoc_food'),
    path('foods/', views.FoodList.as_view(), name='foods_index'),
    path('foods/<int:pk>/', views.FoodDetail.as_view(), name='foods_detail'),
    path('foods/create/', views.FoodCreate.as_view(), name='foods_create'),
    path('foods/<int:pk>/update/', views.FoodUpdate.as_view(), name='foods_update'),
    path('foods/<int:pk>/delete/', views.FoodDelete.as_view(), name='foods_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('finches/<int:finch_id>/add_photo/',
         views.add_photo, name='add_photo'),
]

from django.urls import path
from . import views

app_name = 'drink_app'

urlpatterns = [
    path('', views.drink_list, name='list'),
    path('create/', views.drink_create, name='create'),
]

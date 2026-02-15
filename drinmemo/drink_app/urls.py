from django.urls import path
from . import views

app_name = 'drink_app'

urlpatterns = [
    path('', views.drink_list, name='list'),
    path('create/', views.drink_create, name='create'),
    path('<int:pk>/', views.drink_detail, name='detail'),
    path('<int:pk>/edit/', views.drink_update, name='edit'),
    path('<int:pk>/delete/', views.drink_delete, name='delete'),
]

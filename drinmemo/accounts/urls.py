from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.UserLoginView.as_view(), name='login'),
#     path('activate_user/<uuid:token>', views.activate_user, name='activate_user'),
]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('settings/', views.account_settings, name='settings'),
    path('settings/email/', views.email_change, name='email_change'),

    path('settings/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url='/accounts/settings/?pw=1',
        ),
        name='password_change',
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),

#     path('activate_user/<uuid:token>', views.activate_user, name='activate_user'),
]


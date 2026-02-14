from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate
# from.models import UserActivateToken
# from django.contrib import messages

@login_required
def home(request):
    return render(
        request, 'accounts/home.html'
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        regist_form.save(commit=True)
        return redirect('accounts:home')
    return render(
        request, 'accounts/regist.html', context={
            'regist_form' : regist_form,
        }
    )

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

# def activate_user(request, token):
#     activate_form = forms. UserActivateForm(request.POST or None)
#     if activate_form.is_valid():
#         UserActivateToken.objects.activate_user_by_token(token)
#         messages.success(request, 'ユーザーを有効化しました')
#     activate_form.initial['token'] = token
#     return render(
#         request, 'accounts/activate_user.html', context={
#             'activate_form': activate_form,
#         }
#     )
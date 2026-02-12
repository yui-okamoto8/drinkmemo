from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate


def home(request):
    return render(
        request, "accounts/home.html"
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

def activate_user(request, token):
    pass


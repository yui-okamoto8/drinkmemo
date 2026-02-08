from django.shortcuts import render, redirect
from . import forms

def home(request):
    return render(
        request, "accounts/home.html"
    )

def regist(request):
    regist_form = forms.RegistForm(request.PST or None)
    if regist_form.is_valid():
        regist_form.save(commit=True)
        return redirect('accounts:home')
    return render(
        request, 'accounts/regist.html', context={
            'regist_form' : regist_form,
        }
    )
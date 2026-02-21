from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsernameChangeForm, EmailChangeForm
from django.contrib.auth import login

@login_required
def home(request):
    return render(
        request, 'accounts/home.html'
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        user = regist_form.save(commit=True)
        login(request, user)
        return redirect('accounts:home')
    
    return render(
        request, 'accounts/regist.html', context={
            'regist_form' : regist_form,
        }
    )

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

@login_required
def account_settings(request):
    user = request.user

    # モーダル
    username_form = UsernameChangeForm(instance=user)

    if request.method == "POST":
        # ユーザー名変更だけこの画面
        username_form = UsernameChangeForm(request.POST, instance=user)
        if username_form.is_valid():
            username_form.save()
            messages.success(request, "アカウント名を変更できました")
            return redirect("accounts:settings")
        else:
            messages.error(request, "入力内容を確認してください")

    if request.GET.get("pw") == "1":
        messages.success(request, "パスワードを変更できました")

    if request.GET.get("email") == "1":
        messages.success(request, "メールアドレスを変更できました")

    return render(request, "accounts/settings.html", {
        "username_form": username_form,
    })


@login_required
def email_change(request):
    user = request.user
    form = EmailChangeForm(instance=user)

    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/accounts/settings/?email=1")

    return render(request, "accounts/email_change.html", {"form": form})


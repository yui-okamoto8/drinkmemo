from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsernameChangeForm, EmailChangeForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash

User = get_user_model()

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

# パスワード再設定
def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            request.session["reset_user_id"] = user.id
            return redirect("accounts:password_reset_confirm")
        except User.DoesNotExist:
            messages.error(request, "そのメールアドレスは登録されていません。")

    return render(request, "accounts/password_reset.html")

def password_reset_confirm(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("accounts:login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "パスワードが一致しません。")
        else:
            user.set_password(password1)
            user.save()
            del request.session["reset_user_id"]
            return redirect("accounts:login")

    return render(request, "accounts/password_reset_confirm.html")


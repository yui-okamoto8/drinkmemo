from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistForm(forms.ModelForm):

    confirm_password = forms.CharField(
        label='パスワード再入力', 
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username' : '名前',
            'email' : 'メールアドレス',
            'password' : 'パスワード'
        }
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'password': forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ["username", "email", "password"]:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('password', 'パスワードが一致しません')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        
        user.is_active = True
        
        if commit:
            user.save()
        return user
    
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "アカウント名"}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "メールアドレス"}
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"})
        }



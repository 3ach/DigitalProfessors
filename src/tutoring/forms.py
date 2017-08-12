from django import forms
from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'style': 'margin-bottom: -1; border-bottom-right-radius: 0; border-bottom-left-radius: 0'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'border-top-right-radius: 0; border-top-left-radius: 0'}))

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}
    ))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}
    ))
    username = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
    email = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')

from django import forms
from tutoring.models import Client
from users.models import User, Tutor


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
    email = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ClientForm(UserForm):
    address = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Address'}
    ))
    phone = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
    ))
    website = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Website'}
    ))
    wifi_ssid = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Wi-Fi SSID'}
    ))
    wifi_password = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Wi-Fi Password'}
    ))

    def save(self, commit=True):
        user = super(ClientForm, self).save(commit)

        if commit:
            client = Client.objects.filter(user=user)

            if client.exists():
                client.update(address=self.cleaned_data['address'], phone=self.cleaned_data['phone'],
                              wifi_ssid=self.cleaned_data['wifi_ssid'], wifi_password=self.cleaned_data['wifi_password'],)
            else:
                client = Client.objects.create(address=self.cleaned_data['address'], phone=self.cleaned_data['phone'],
                                           wifi_ssid=self.cleaned_data['wifi_ssid'], wifi_password=self.cleaned_data['wifi_password'], user=user)
            client.save()

        return user


class TutorForm(UserForm):

    def save(self, commit=True):
        user = super(TutorForm, self).save(commit)

        if commit:
            tutor = Tutor.objects.create(user=user)
            tutor.save()

        return user

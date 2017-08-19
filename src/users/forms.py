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

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        
        if kwargs['instance']:
            client = Client.objects.get(user=kwargs['instance'])

            self.initial['address'] = client.address
            self.initial['phone'] = client.phone
            self.initial['website'] = client.website
            self.initial['wifi_ssid'] = client.wifi_ssid
            self.initial['wifi_password'] = client.wifi_password
        
    def save(self, commit=True):
        user = super(ClientForm, self).save(commit)

        if commit:
            client, created = Client.objects.get_or_create(user=user)

            if self.cleaned_data['address']:
                client.address = self.cleaned_data['address']
            
            if self.cleaned_data['phone']:
                client.phone = self.cleaned_data['phone']

            if self.cleaned_data['website']:
                client.website = self.cleaned_data['website']

            if self.cleaned_data['wifi_ssid']:
                client.wifi_ssid = self.cleaned_data['wifi_ssid']

            if self.cleaned_data['wifi_password']:
                client.wifi_password = self.cleaned_data['wifi_password']

            client.save()
            

        return user


class TutorForm(UserForm):
    wage = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Wage'}))

    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)

        if kwargs['instance']:
            tutor = Tutor.objects.get(user=kwargs['instance'])

            self.initial['wage'] = tutor.wage
    def save(self, commit=True):
        user = super(TutorForm, self).save(commit)

        if commit:
            tutor, created = Tutor.objects.get_or_create(user=user)

            if self.cleaned_data['wage']:
                tutor.wage = self.cleaned_data['wage']

            tutor.save()

        return user

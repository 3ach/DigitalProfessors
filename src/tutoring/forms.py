from django import forms
from django.conf import settings
from tutoring.models import Session, Client, Professor, SessionCategory


class SessionForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select Client", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), empty_label="Select Professor", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    category = forms.ModelChoiceField(queryset=SessionCategory.objects.all(), empty_label="Select Category", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'date'}))

    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'time'}, format="%I:%M %p"))

    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'placeholder': 'End Time', 'type': 'time'}, format="%I:%M %p"))

    distance = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Distance'}))

    hourly = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hourly Rate', 'type': 'number'}))

    billed = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billed', 'readonly': 'readonly'}))

    paid = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Paid'}))
    
    payment_method = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=settings.CHARGE_METHODS)

    class Media:
        js = ('js/session.js', )

    class Meta:
        model = Session
        exclude = ('earnings', 'earnings_paid', 'notes', )

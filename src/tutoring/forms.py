from django import forms
from tutoring.models import Session, Client, Tutor


class SessionForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select Client", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    tutor = forms.ModelChoiceField(queryset=Tutor.objects.all(), empty_label="Select Tutor", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'date'}))

    start_time = forms.TimeField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'time'}))

    end_time = forms.TimeField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'End Time', 'type': 'time'}))

    distance = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Distance'}))

    hourly = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hourly Rate', 'type': 'number'}))

    billed = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billed', 'readonly': 'readonly'}))

    paid = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Paid'}))

    class Media:
        js = ('js/session.js', )

    class Meta:
        model = Session
        exclude = ()

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from tutoring.models import Session, Client, Tutor


class SessionForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select Client", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    tutor = forms.ModelChoiceField(queryset=Tutor.objects.all(), empty_label="Select Tutor", widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    time = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "icons": {
        "time": 'fa fa-clock-o',
        "date": 'fa fa-calendar',
        "up": 'fa fa-chevron-circle-up',
        "down": 'fa fa-chevron-circle-down',
        "previous": 'fa fa-chevron-circle-left',
        "next": 'fa fa-chevron-circle-right',
        "today": 'fa fa-calendar-times-o',
        "clear": 'fa fa-trash',
        "close": 'fa fa-times'
    }, }, attrs={'class': 'form-control', 'placeholder': 'Date and Time'}))
    distance = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Distance'}))
    billed = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billed'}))
    paid = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Paid'}))

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', )}
        js = ('js/moment-with-locales.min.js',
              'js/bootstrap-datetimepicker.min.js')

    class Meta:
        model = Session
        fields = ('client', 'tutor', 'time', 'distance', 'billed', 'paid')

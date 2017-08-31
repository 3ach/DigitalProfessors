from urllib.parse import urlencode
from django.conf import settings
from django.db import models
from datetime import datetime, date
from decimal import Decimal

class SessionCategory(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Session(models.Model):
    client = models.ForeignKey("Client")
    professor = models.ForeignKey("Professor")
    category = models.ForeignKey("SessionCategory")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    distance = models.FloatField()
    payment_method = models.CharField(max_length=4, choices=settings.CHARGE_METHODS)
    hourly = models.DecimalField(max_digits=12, decimal_places=2)
    billed = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    earnings_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)

    @property
    def remaining(self):
        return self.billed - self.paid

    @property
    def earnings_remaining(self):
        return self.earnings - self.earnings_paid

    def save(self, *args, **kwargs):
        duration = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        hours = duration.total_seconds() / (60 * 60)
        hours = round(hours * 2) / 2
        self.earnings = Decimal(hours) * self.professor.wage

        if self.earnings < 15:
            self.earnings = 15

        return super(Session, self).save(*args, **kwargs)

class Client(models.Model):
    user = models.ForeignKey('users.User')
    address = models.TextField(blank=True, null=True)
    phone = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    wifi_ssid = models.TextField(max_length=128, blank=True, null=True)
    wifi_password = models.TextField(max_length=128, blank=True, null=True)

    @property
    def map_url(self):
        base_url = 'https://maps.googleapis.com/maps/api/staticmap?{}'
        args = {
            'center': self.address,
            'zoom': 15,
            'size': '600x100',
            'scale': 2,
            'markers': "|" + self.address,
            'key': settings.GOOGLE_MAPS_STATIC_API_KEY
        }

        return base_url.format(urlencode(args))

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def formatted_phone(self):
        phone = str(self.phone)
        if len(phone) != 10:
            return self.phone

        return '(' + phone[0:3] + ') ' + phone[3:6] + '-' + phone[6:]

    def save(self, *args, **kwargs):
        if self.website and self.website[0:7] != "http://":
            self.website = 'http://' + self.website

        return super(Client, self).save(*args, **kwargs)

class Professor(models.Model):
    wage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    user = models.ForeignKey("users.User")

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

from urllib.parse import urlencode
from django.conf import settings
from django.db import models

class Session(models.Model):
    client = models.ForeignKey("Client")
    tutor = models.ForeignKey("Tutor")
    time = models.DateTimeField()
    distance = models.FloatField()
    billed = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.DecimalField(max_digits=12, decimal_places=2)

class Client(models.Model):
    user = models.ForeignKey('users.User')
    address = models.TextField()
    phone = models.IntegerField()
    website = models.URLField()
    wifi_ssid = models.TextField(max_length=128)
    wifi_password = models.TextField(max_length=128)

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


class Tutor(models.Model):
    user = models.ForeignKey("users.User")

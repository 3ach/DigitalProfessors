from django.contrib.auth.models import AbstractUser
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse_lazy
from tutoring.models import Tutor, Client


class User(AbstractUser): 
    def _userlevel(self, result):
        if self.is_staff:
            return result['manager']
        elif Tutor.objects.filter(user=self).exists():
            return result['tutor']
        elif Client.objects.filter(user=self).exists():
            return result['client']
        else:
            raise SuspiciousOperation

    @property
    def usertype(self):
        if self.is_staff:
            return 'manager'
        elif Tutor.objects.filter(user=self).exists():
            return 'tutor'
        elif Client.objects.filter(user=self).exists():
            return 'client'
        else:
            raise SuspiciousOperation

    @property
    def nav_links(self):
        return self._userlevel({
            'client': [],
            'tutor': [
                {
                    "name": "Clients",
                    "url": "clients"
                }
            ],
            'manager': [
                {
                    "name": "Accounting",
                    "url": "accounting"
                },
                {
                    "name": "Clients",
                    "url": "clients"
                },
                {
                    "name": "Tutors",
                    "url": "tutors"
                }
            ]
        })

    @property
    def dashboard(self):
        return self._userlevel({
            'client': reverse_lazy('client-dashboard'),
            'tutor': reverse_lazy('tutor-dashboard'),
            'manager': reverse_lazy('manager-dashboard')
        })

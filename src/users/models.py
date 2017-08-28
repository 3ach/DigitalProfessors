from django.contrib.auth.models import AbstractUser
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse_lazy
from tutoring.models import Professor, Client


class User(AbstractUser): 
    def _userlevel(self, result):
        if self.is_staff:
            return result['manager']
        elif Professor.objects.filter(user=self).exists():
            return result['professor']
        elif Client.objects.filter(user=self).exists():
            return result['client']
        else:
            raise SuspiciousOperation

    @property
    def usertype(self):
        if self.is_staff:
            return 'manager'
        elif Professor.objects.filter(user=self).exists():
            return 'professor'
        elif Client.objects.filter(user=self).exists():
            return 'client'
        else:
            raise SuspiciousOperation

    @property
    def nav_links(self):
        return self._userlevel({
            'client': [
                {
                    "name": "Accounting",
                    "url": "accounting"
                },
            ],
            'professor': [
                {
                    "name": "Accounting",
                    "url": "accounting"
                },
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
                    "name": "Professors",
                    "url": "professors"
                },
                {
                    "name": "Admin",
                    "url": "admin:index"
                }
            ]
        })

    @property
    def dashboard(self):
        return self._userlevel({
            'client': reverse_lazy('client-dashboard'),
            'professor': reverse_lazy('professor-dashboard'),
            'manager': reverse_lazy('manager-dashboard')
        })

    @property
    def accounting(self):
        return self._userlevel({
            'client': reverse_lazy('client-accounting'),
            'professor': reverse_lazy('professor-accounting'),
            'manager': reverse_lazy('manager-accounting')
        })

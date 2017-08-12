from django.contrib import admin
from tutoring.models import Client, Session, Tutor

# Register your models here.
admin.site.register(Client)
admin.site.register(Session)
admin.site.register(Tutor)
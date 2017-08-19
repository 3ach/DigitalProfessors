from django.contrib import admin
from tutoring.models import Client, Session, Tutor, SessionCategory

# Register your models here.
admin.site.register(Client)
admin.site.register(Session)
admin.site.register(SessionCategory)
admin.site.register(Tutor)
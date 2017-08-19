from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^login', views.LoginView.as_view(), name="login"),
    url(r'^logout', views.LogoutView.as_view(), name="logout"),
    url(r'^clients/new', views.AddClientView.as_view(), name="add-client"),
    url(r'^clients/(?P<pk>[0-9]+)', views.UpdateClientView.as_view(), name="edit-client"),
    url(r'^tutors/new', views.AddTutorView.as_view(), name="add-tutor"),
    url(r'^tutors/(?P<pk>[0-9]+)', views.UpdateTutorView.as_view(), name="edit-tutor"),
    url(r'^users/(?P<pk>[0-9]+)/delete', views.DeleteUserView.as_view(), name="delete-user"),
    url(r'^users/(?P<pk>[0-9]+)', views.UserFormView.as_view(), name="edit-user")
]

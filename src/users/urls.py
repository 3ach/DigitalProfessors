from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^login', views.LoginView.as_view(), name="login"),
    url(r'^logout', views.LogoutView.as_view(), name="logout"),
    url(r'^clients/new', views.AddClientView.as_view(), name="add-client"),
    url(r'^clients/(?P<pk>[0-9]+)', views.UpdateClientView.as_view(), name="edit-client"),
    url(r'^professors/new', views.AddProfessorView.as_view(), name="add-professor"),
    url(r'^professors/(?P<professor_id>[0-9]+)/deactivate', views.DeactivateProfessorView.as_view(), name="deactivate-professor"),
    url(r'^professors/(?P<pk>[0-9]+)', views.UpdateProfessorView.as_view(), name="edit-professor"),
    url(r'^users/(?P<pk>[0-9]+)/delete', views.DeleteUserView.as_view(), name="delete-user"),
    url(r'^users/(?P<pk>[0-9]+)', views.UserFormView.as_view(), name="edit-user"),
    url(r'^setup', views.SetupView.as_view(), name="setup-manager")
]

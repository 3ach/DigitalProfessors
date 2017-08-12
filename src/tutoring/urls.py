from django.conf.urls import url, include
from django.contrib import admin
from tutoring import views

dashboards = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^manager', views.ManagerDashboardView.as_view(), name="manager-dashboard"),
    url(r'^client', views.ClientDashboardView.as_view(), name="client-dashboard"),
    url(r'^tutor', views.TutorDashboardView.as_view(), name="tutor-dashboard")
]

urlpatterns = [
    url(r'^login', views.LoginView.as_view(), name="login"),
    url(r'^logout', views.LogoutView.as_view(), name="logout"),
    url(r'^accounting', views.AccountingView.as_view(), name="accounting"),
    url(r'^accounting/(?P<user_id>[0-9]+)', views.UserAccountingView.as_view(), name="accounting-detail"),
    url(r'^users/(?P<pk>[0-9]+)', views.UserFormView.as_view(), name="edit-user"),
    url(r'^clients', views.ClientsView.as_view(), name="clients"),
    url(r'^tutors', views.TutorsView.as_view(), name="tutors"),
    url(r'^dashboard/', include(dashboards)),
    url(r'^$', views.DashboardView.as_view())
]

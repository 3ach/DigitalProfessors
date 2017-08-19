from django.conf.urls import url, include
from django.contrib import admin
from tutoring import views

dashboards = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^manager', views.ManagerDashboardView.as_view(), name="manager-dashboard"),
    url(r'^client', views.ClientDashboardView.as_view(), name="client-dashboard"),
    url(r'^tutor', views.TutorDashboardView.as_view(), name="tutor-dashboard")
]

accounting = [
    url(r'^$', views.AccountingView.as_view(), name="accounting"),
    url(r'^manager', views.ManagerAccountingView.as_view(), name="manager-accounting"),
    url(r'^client', views.ClientAccountingView.as_view(), name="client-accounting"),
    url(r'^tutor', views.TutorAccountingView.as_view(), name="tutor-accounting"),
    url(r'^user/(?P<user_id>[0-9]+)', views.UserAccountingView.as_view(), name="accounting-detail"),
]

urlpatterns = [
    url(r'^session/(?P<session_id>[0-9]+)/earnings', views.SessionEarningsUpdate.as_view(), name="session-notes"),
    url(r'^session/(?P<session_id>[0-9]+)/payment', views.SessionPaymentUpdate.as_view(), name="session-notes"),
    url(r'^session/(?P<session_id>[0-9]+)/notes', views.SessionNoteUpdate.as_view(), name="session-notes"),
    url(r'^session/(?P<session_id>[0-9]+)/', views.SessionView.as_view(), name="session-detail"),
    url(r'^clients', views.ClientsView.as_view(), name="clients"),
    url(r'^tutors', views.TutorsView.as_view(), name="tutors"),
    url(r'^sessions/new', views.CreateSessionView.as_view(), name="add-session"),
    url(r'^csv/', views.CSVUploadView.as_view(), name="csv-upload"),
    url(r'^dashboard/', include(dashboards)),
    url(r'^accounting/', include(accounting)),
    url(r'^$', views.DashboardView.as_view())
]

from django.conf.urls import url, include
from django.contrib import admin
from tutoring import views

dashboards = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^manager', views.ManagerDashboardView.as_view(), name="manager-dashboard"),
    url(r'^client', views.ClientDashboardView.as_view(), name="client-dashboard"),
    url(r'^professor', views.ProfessorDashboardView.as_view(), name="professor-dashboard")
]

accounting = [
    url(r'^$', views.AccountingView.as_view(), name="accounting"),
    url(r'^manager', views.ManagerAccountingView.as_view(), name="manager-accounting"),
    url(r'^client', views.ClientAccountingView.as_view(), name="client-accounting"),
    url(r'^professor', views.ProfessorAccountingView.as_view(), name="professor-accounting"),
    url(r'^user/(?P<user_id>[0-9]+)', views.UserAccountingView.as_view(), name="accounting-detail"),
]

urlpatterns = [
    url(r'^session/(?P<session_id>[0-9]+)/earnings', views.SessionEarningsUpdate.as_view(), name="session-earnings"),
    url(r'^session/(?P<session_id>[0-9]+)/payment', views.SessionPaymentUpdate.as_view(), name="session-payment"),
    url(r'^session/(?P<session_id>[0-9]+)/notes', views.SessionNoteUpdate.as_view(), name="session-notes"),
    url(r'^session/(?P<session_id>[0-9]+)/cancel', views.CancelSessionView.as_view(), name="session-cancel"),
    url(r'^session/(?P<session_id>[0-9]+)/updateSession', views.UpdateStatusView.as_view(), name="status"),
    url(r'^session/(?P<session_id>[0-9]+)/', views.SessionView.as_view(), name="session-detail"),
    url(r'^clients/(?P<client_id>[0-9]+)/sessions', views.ClientSessionsView.as_view(), name='client-sessions'),
    url(r'^clients', views.ClientsView.as_view(), name="clients"),
    url(r'^professors/(?P<professor_id>[0-9]+)/sessions', views.ProfessorSessionsView.as_view(), name='professor-sessions'),
    url(r'^professors', views.ProfessorsView.as_view(), name="professors"),
    url(r'^sessions/new', views.CreateSessionView.as_view(), name="add-session"),
    url(r'^csv/', views.CSVUploadView.as_view(), name="csv-upload"),
    url(r'^dashboard/', include(dashboards)),
    url(r'^accounting/', include(accounting)),
    url(r'^$', views.DashboardView.as_view())
]

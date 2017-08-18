from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView, DeleteView, CreateView
from tutoring.models import Tutor, Client, Session
from tutoring.forms import SessionForm
from users.models import User

@method_decorator(login_required, name='dispatch')
class ManagerDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(ManagerDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.all()

        return context

@method_decorator(login_required, name='dispatch')
class AccountingView(TemplateView):
    template_name = "tutoring/accounting.html"

@method_decorator(login_required, name='dispatch')
class ClientsView(TemplateView):
    template_name = "tutoring/clients.html"

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        context["clients"] = Client.objects.all().order_by('user__last_name')

        return context

@method_decorator(login_required, name='dispatch')
class TutorsView(TemplateView):
    template_name = "tutoring/tutors.html"

    def get_context_data(self, **kwargs):
        context = super(TutorsView, self).get_context_data(**kwargs)
        context["tutors"] = Tutor.objects.all().order_by('user__last_name')

        return context

@method_decorator(login_required, name='dispatch')
class UserAccountingView(TemplateView):
    pass

@method_decorator(login_required, name='dispatch')
class TutorDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(TutorDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(tutor__user=user)

        return context

@method_decorator(login_required, name='dispatch')
class ClientDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ClientDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(client__user=user)

        return context

@method_decorator(login_required, name='dispatch')
class SessionView(TemplateView):
    template_name = "tutoring/session.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(SessionView, self).get_context_data(**kwargs)
        
        return context

@method_decorator(login_required, name='dispatch')
class CreateSessionView(CreateView):
    model = Session
    template_name = 'tutoring/session-form.html'
    form_class = SessionForm
    success_url = reverse_lazy('dashboard')

@method_decorator(login_required, name='dispatch')
class DashboardView(RedirectView):
    """
    Redirects the user to the appropriate dashboard
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        print("getting redirect url")

        return user.dashboard

from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView
from tutoring.forms import LoginForm, UserForm
from tutoring.models import Tutor, Client, Session
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
class UserFormView(UpdateView):
    model = User
    template_name = 'tutoring/user-form.html'
    form_class = UserForm
    success_url = 'accounting'

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
class DashboardView(RedirectView):
    """
    Redirects the user to the appropriate dashboard
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        print("getting redirect url")

        return user.dashboard


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = LoginForm
    template_name = 'tutoring/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]

        user = authenticate(request=self.request, username=username, password=password)

        if user is None:
            pass

        login(self.request, user)

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            redirect_to = self.request.GET[self.redirect_field_name]
        except KeyError:
            redirect_to = self.success_url

        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url

        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

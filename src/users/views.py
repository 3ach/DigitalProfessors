from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect
from tutoring.models import Tutor, Client, Session
from users.forms import LoginForm, UserForm, ClientForm, TutorForm
from users.models import User

@method_decorator(login_required, name='dispatch')
class UserFormView(UpdateView):
    model = User
    template_name = 'users/user-form.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard')

@method_decorator(login_required, name='dispatch')
class UpdateClientView(UpdateView):
    model = User
    template_name = 'users/user-form.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients')

@method_decorator(login_required, name='dispatch')
class UpdateTutorView(UpdateView):
    model = User
    template_name = 'users/user-form.html'
    form_class = TutorForm
    success_url = reverse_lazy('tutors')

@method_decorator(login_required, name='dispatch')
class AddClientView(CreateView):
    model = User
    template_name = 'users/user-form.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients')

@method_decorator(login_required, name='dispatch')
class AddTutorView(CreateView):
    model = User
    template_name = 'users/user-form.html'
    form_class = TutorForm
    success_url = reverse_lazy('tutors')

@method_decorator(login_required, name='dispatch')
class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('dashboard')

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = LoginForm
    template_name = 'users/login.html'
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

        if user is None or not user.is_authenticated:
            return redirect('/users/login/?next=/')
        
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

@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

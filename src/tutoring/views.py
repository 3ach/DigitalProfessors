from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView, DeleteView, CreateView, View
from tutoring.models import Professor, Client, Session
from tutoring.forms import SessionForm
from users.models import User
from csv import DictReader
from decimal import Decimal
import io
import json

@method_decorator(login_required, name='dispatch')
class AccountingView(RedirectView):
    """
    Redirects the user to the appropriate dashboard
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        return user.accounting

@method_decorator(login_required, name='dispatch')
class ManagerAccountingView(TemplateView):
    template_name = 'tutoring/accounting-manager.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerAccountingView, self).get_context_data(**kwargs)

        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET['start']
            end = self.request.GET['end']
            
            base = Session.objects.filter(date__gte=start).filter(date__lte=end)
        else:
            base = Session.objects.all()

        aggregates = base.aggregate(Sum('billed'), Sum('paid'), Sum('earnings'), Sum('earnings_paid'))
        unpaid = base.exclude(billed=F('paid')).values('client').annotate(Sum('billed')).annotate(Sum('paid'))
        owed = base.exclude(earnings=F('earnings_paid')).values('professor').annotate(Sum('earnings')).annotate(Sum('earnings_paid'))

        try:
            for client in unpaid: 
                client['client'] = Client.objects.get(id=client["client"])
                client['total_owed'] = client['billed__sum'] - client['paid__sum']

            for professor in owed:
                professor['professor'] = Professor.objects.get(id=professor['professor'])
                professor['total_owed'] = professor['earnings__sum'] - professor['earnings_paid__sum']

            context['billed'] = aggregates['billed__sum']
            context['received'] = aggregates['paid__sum']
            context['due'] = context['billed'] - context['received']
            context['gross'] = context['billed']
            context['owed'] = aggregates['earnings__sum']
            context['paid'] = aggregates['earnings_paid__sum']
            context['earnings_due'] = context['owed'] - context['paid']
            context['net'] = context['gross'] - context['owed']
            context['unpaid'] = unpaid
            context['professorsOwed'] = owed
            
            return context
        except TypeError:
            return context

@method_decorator(login_required, name='dispatch')
class ProfessorAccountingView(TemplateView):
    template_name = 'tutoring/accounting-professor.html'
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProfessorAccountingView, self).get_context_data(**kwargs)

        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET['start']
            end = self.request.GET['end']
            
            base = Session.objects.filter(date__gte=start).filter(date__lte=end)
        else:
            base = Session.objects.all()        

        aggregates = base.filter(professor__user=user.id).aggregate(Sum('billed'), Sum('paid'), Sum('earnings'), Sum('earnings_paid'))
        unpaid = base.filter(professor__user=user).exclude(billed=F('paid'))

        try:
            context['billed'] = aggregates['earnings__sum']
            context['received'] = aggregates['earnings_paid__sum']
            context['due'] = context['billed'] - context['received']
            context['unpaid'] = unpaid
            
            return context
        except TypeError:
            return context

@method_decorator(login_required, name='dispatch')
class ClientAccountingView(TemplateView):
    template_name = 'tutoring/accounting-client.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ClientAccountingView, self).get_context_data(**kwargs)

        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET['start']
            end = self.request.GET['end']
            
            base = Session.objects.filter(date__gte=start).filter(date__lte=end)
        else:
            base = Session.objects.all()

        aggregates = base.filter(client__user=user.id).aggregate(Sum('billed'), Sum('paid'), Sum('earnings'), Sum('earnings_paid'))
        unpaid = base.filter(client__user=user).exclude(billed=F('paid'))

        try:
            context['billed'] = aggregates['billed__sum']
            context['received'] = aggregates['paid__sum']
            context['due'] = context['billed'] - context['received']
            context['unpaid'] = unpaid
            
            return context
        except TypeError:
            return context

@method_decorator(login_required, name='dispatch')
class UserAccountingView(TemplateView):
    pass

@method_decorator(login_required, name='dispatch')
class ClientsView(TemplateView):
    template_name = "tutoring/clients.html"

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        context["clients"] = Client.objects.all().order_by('user__last_name')

        return context

@method_decorator(login_required, name='dispatch')
class ProfessorsView(TemplateView):
    template_name = "tutoring/professors.html"

    def get_context_data(self, **kwargs):
        context = super(ProfessorsView, self).get_context_data(**kwargs)
        context["professors"] = Professor.objects.all().order_by('user__last_name')

        return context

@method_decorator(login_required, name='dispatch')
class ProfessorDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProfessorDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(professor__user=user).order_by('-date')

        return context

@method_decorator(login_required, name='dispatch')
class ClientDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ClientDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(client__user=user).order_by('-date')

        return context

@method_decorator(login_required, name='dispatch')
class ManagerDashboardView(TemplateView):
    template_name = "tutoring/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(ManagerDashboardView, self).get_context_data(**kwargs)
        context["sessions"] = Session.objects.all().order_by('-date')

        return context

@method_decorator(login_required, name='dispatch')
class SessionView(TemplateView):
    template_name = "tutoring/session.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        session_id = kwargs['session_id']
        session = Session.objects.get(id=session_id)

        context = super(SessionView, self).get_context_data(**kwargs)
        context['session'] = session
        
        return context

@method_decorator(login_required, name='dispatch')
class CreateSessionView(CreateView):
    model = Session
    template_name = 'tutoring/session-form.html'
    form_class = SessionForm
    
    def get_success_url(self):
        return reverse_lazy('session-detail', args=(self.object.id, ))

@method_decorator(login_required, name='dispatch')
class DashboardView(RedirectView):
    """
    Redirects the user to the appropriate dashboard
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        return user.dashboard

@method_decorator(login_required, name='dispatch')
class CSVUploadView(TemplateView):
    template_name = 'tutoring/csv-form.html'

    def post(self, request):
        post = request.POST
        csvfile = request.FILES['csvFile'].file
        csvfile = csvfile.read().decode('utf8', 'ignore')
        headers = json.loads(request.POST['headers'])

        reader = DictReader(io.StringIO(csvfile), headers);

        for index, row in enumerate(reader):
            if index == 0:
                continue

            client = Client()
            user = User()

            user.first_name = row[headers[int(post['firstName'])]]
            user.last_name = row[headers[int(post['lastName'])]]
            user.email = row[headers[int(post['email'])]]

            if post['username'] == 'generate':
                user.username = row[headers[int(post['firstName'])]].lower() + row[headers[int(post['lastName'])]].lower()
            else: 
                user.username = row[headers[int(post['username'])]]
            
            user.save()
            user.set_password(row[headers[int(post['phone'])]])
            user.save()

            client.address = row[headers[int(post['address'])]]
            client.phone = row[headers[int(post['phone'])]]
            client.website = row[headers[int(post['website'])]]
            client.wifi_ssid = row[headers[int(post['ssid'])]]
            client.wifi_password = row[headers[int(post['password'])]]
            client.user = user

            client.save()

        return redirect(reverse_lazy('clients'))

class SessionNoteUpdate(View):
    def post(self, request, session_id):
        notes = request.POST['notes']
        session = Session.objects.get(id=session_id)

        session.notes = notes
        session.save()

        return HttpResponse(status=200)

class SessionPaymentUpdate(View):
    def post(self, request, session_id):
        payment = request.POST['payment']
        session = Session.objects.get(id=session_id)

        session.paid += Decimal(payment)
        session.save()

        return HttpResponse(status=200)

class SessionEarningsUpdate(View):
    def post(self, request, session_id):
        payment = request.POST['payment']
        session = Session.objects.get(id=session_id)

        session.earnings_paid += Decimal(payment)
        session.save()

        return HttpResponse(status=200)


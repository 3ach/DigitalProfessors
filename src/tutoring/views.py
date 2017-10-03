from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
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
from tutoring.forms import SessionForm, ContactForm, StatusForm
from users.models import User
from csv import DictReader
from decimal import Decimal
import io
import json
import re

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
        
        cash_gross = base.filter(payment_method="CASH").aggregate(Sum('billed'))
        credit_gross = base.filter(payment_method="CRDT").aggregate(Sum('billed'))
        check_gross = base.filter(payment_method="CHCK").aggregate(Sum('billed'))

        try:
            for client in unpaid: 
                client['client'] = Client.objects.get(id=client["client"])
                client['total_owed'] = client['billed__sum'] - client['paid__sum']

            for professor in owed:
                professor['professor'] = Professor.objects.get(id=professor['professor'])
                professor['total_owed'] = professor['earnings__sum'] - professor['earnings_paid__sum']

            context['billed'] = aggregates['billed__sum'] if aggregates["billed__sum"] is not None else 0
            context['received'] = aggregates['paid__sum'] if aggregates["paid__sum"] is not None else 0
            context['due'] = context['billed'] - context['received']
            context['gross_check'] = check_gross['billed__sum'] if check_gross['billed__sum'] is not None else 0
            context['gross_cash'] = cash_gross['billed__sum'] if cash_gross['billed__sum'] is not None else 0
            context['gross_credit'] = credit_gross['billed__sum'] if credit_gross['billed__sum'] is not None else 0
            context['owed'] = aggregates['earnings__sum'] if aggregates["earnings__sum"] is not None else 0
            context['paid'] = aggregates['earnings_paid__sum'] if aggregates["earnings_paid__sum"] is not None else 0
            context['earnings_due'] = context['owed'] - context['paid']
            context['net'] = context['billed'] - context['owed']
            context['unpaid'] = unpaid
            context['professorsOwed'] = owed
            
        except TypeError:
            pass
        
        for item in context:
            if context[item] == 0:
                context[item] = "0.00"

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
            context['billed'] = aggregates['earnings__sum'] if aggregates["earnings__sum"] is not None else 0
            context['received'] = aggregates['earnings_paid__sum'] if aggregates["earnings_paid__sum"] is not None else 0
            context['due'] = context['billed'] - context['received']
            context['unpaid'] = unpaid
            
        except TypeError:
            pass
        
        for item in context:
            if context[item] is 0:
                context[item] = "0.00"

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
            context['billed'] = aggregates['billed__sum'] if aggregates["billed__sum"] is not None else 0
            context['received'] = aggregates['paid__sum'] if aggregates["paid__sum"] is not None else 0
            context['due'] = context['billed'] - context['received']
            context['unpaid'] = unpaid

        except TypeError:
            pass
        
        for item in context:
            if context[item] is 0:
                context[item] = "0.00"

        return context

@method_decorator(login_required, name='dispatch')
class UserAccountingView(TemplateView):
    pass
    

@method_decorator(login_required, name='dispatch')
class ProfessorSessionsView(TemplateView):
    template_name = 'tutoring/professor-sessions.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProfessorSessionsView, self).get_context_data(**kwargs)
        professor = Professor.objects.get(id=kwargs['professor_id'])
        context["professor"] = professor
        context["sessions"] = Session.objects.filter(professor=professor).order_by('-date')

        return context

@method_decorator(login_required, name='dispatch')
class ClientSessionsView(TemplateView):
    template_name = 'tutoring/client-sessions.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ClientSessionsView, self).get_context_data(**kwargs)
        client = Client.objects.get(id=kwargs['client_id'])
        context["client"] = client
        context["sessions"] = Session.objects.filter(client=client).order_by('-date')

        return context

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

        status = "OPEN"
        if "status" in self.request.GET:
            status = self.request.GET["status"]

        context["sessions"] = Session.objects.filter(professor__user=user, status=status).order_by('-date')
        context["status_form"] = StatusForm()
        context['status_form'].fields['status'].initial = status

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

        status = "OPEN"
        if "status" in self.request.GET:
            status = self.request.GET["status"]
        
        context["sessions"] = Session.objects.filter(status=status).order_by('-date')
        context["status_form"] = StatusForm()
        context['status_form'].fields['status'].initial = status

        return context

@method_decorator(login_required, name='dispatch')
class SessionView(TemplateView):
    template_name = "tutoring/session.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        session_id = kwargs['session_id']
        session = Session.objects.get(id=session_id)

        context = super(SessionView, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['status_form'] = StatusForm()
        context['session'] = session
        context['status_form'].fields['status'].initial = session.status
        
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(self.request.POST)

        if form.is_valid():
            send_mail(
                'Client Question',
                form.cleaned_data['message'],
                'digitalprofessors@digitalprofessors.com',
                ['josh.glyn@gmail.com'],
                fail_silently=True,
            )

        return super(SessionView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CreateSessionView(CreateView):
    model = Session
    template_name = 'tutoring/session-form.html'
    form_class = SessionForm
    
    def get_success_url(self):
        return reverse_lazy('session-detail', args=(self.object.id, ))

    def get_initial(self):
        initial = super(CreateSessionView, self).get_initial()

        if 'client' in self.request.GET:
            initial["client"] = self.request.GET["client"]


        if 'professor' in self.request.GET:
            initial["professor"] = self.request.GET["professor"]

        return initial

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
            row["!!EMPTY!!"] = ""

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
            
            try:
                user.save()
            except IntegrityError:
                continue

            non_decimal = re.compile(r'[^\d.]+')

            phone_number = non_decimal.sub('', row[headers[int(post['phone'])]])
            phone_number = "".join(phone_number.split('.'))

            if phone_number == '':
                phone_number = 0000000000
            else:
                phone_number = int(phone_number)

            client.address = row[headers[int(post['address'])]]
            client.phone = phone_number
            client.website = row[headers[int(post['website'])]]
            client.wifi_ssid = row[headers[int(post['ssid'])]]
            client.wifi_password = row[headers[int(post['password'])]]
            client.user = user

            user.set_password(client.phone)
            user.save()
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

class CancelSessionView(View):
    def post(self, request, session_id):
        session = Session.objects.get(id=session_id)
        session.cancelled = True
        session.billed = 0
        session.earnings = 0

        session.save()

        return redirect(reverse_lazy('session-detail', args=(session.id, )))

class UpdateStatusView(View):
    def post(self, request, session_id):
        status = request.POST['status']
        session = Session.objects.get(id=session_id)
        
        session.status = status
        session.save()

        return redirect(reverse_lazy('session-detail', args=(session.id, )))

from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import TemplateView,FormView,View,CreateView
from .forms import IncomeForm,RegisterForm,MyLoginForm,ExpenseForm,DebtForm
from django.core.exceptions import ValidationError
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from .models import Income,Expenses,Debt
from .multiforms import MultiFormsView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .utils import GetObjectMixin,RegisterLoginPagesMixin,FetchData
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home-user.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.request.user.owner
        income = Income.objects.filter(owner=owner)
        debt = Debt.objects.filter(owner=owner)
        expense = Expenses.objects.filter(owner=owner)
        expense_total = [expense_total.actual_amount for expense_total in expense]
        gross_expense = sum(expense_total)
        debt_total = [debt_total.actual_amount for debt_total in debt]
        gross_debt = sum(debt_total)
        actual_income = [actual_income.actual_amount for actual_income in income]
        gross_income = sum(actual_income)
        net_income = gross_income - gross_debt
        context['expense_total'] = expense_total
        context['actual_income'] = actual_income
        context['debt_total'] = debt_total
        context['gross_income'] = gross_income
        context['gross_debt'] = gross_debt
        context['net_income'] = net_income
        context['gross_expense'] = gross_expense
        return context


class RegisterView(RegisterLoginPagesMixin,CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('budget:home-user')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')

        if password == password2:
            pass
        else:
            raise ValidationError('Password 1 must be equal to 2')

        user = User.objects.create_user(username=uname,email=email,
                                        password=password)
        form.instance.user = user
        login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

    def get_next_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

class AllForms(LoginRequiredMixin,MultiFormsView):
    template_name = 'forms.html'
    login_url = 'budget:login'
    redirect_field_name = 'budget:login'
   
    form_classes = {'income': IncomeForm,
                    'expense': ExpenseForm,
                    'debt': DebtForm,
                    }

    success_urls = {
        'income': reverse_lazy('budget:forms'),
        'expense': reverse_lazy('budget:forms'),
        'debt': reverse_lazy('budget:forms'),
    }

    def income_form_valid(self, form):
        source = form.cleaned_data.get('source')
        planned_amount = form.cleaned_data.get('planned_amount')
        actual_amount = form.cleaned_data.get('actual_amount')
        form_name = form.cleaned_data.get('action')
        form.instance.owner = self.request.user.owner
        form.instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))
    
    def expense_form_valid(self, form):
        category = form.cleaned_data.get('category')
        name_of_expense = form.cleaned_data.get('name_of_expense')
        planned_amount = form.cleaned_data.get('planned_amount')
        actual_amount = form.cleaned_data.get('actual_amount')
        form_name = form.cleaned_data.get('action')
        form.instance.owner = self.request.user.owner
        form.instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))

    def debt_form_valid(self, form):
        paid_to = form.cleaned_data.get('paid_to')
        planned_amount = form.cleaned_data.get('planned_amount')
        actual_amount = form.cleaned_data.get('actual_amount')
        form_name = form.cleaned_data.get('action')
        form.instance.owner = self.request.user.owner
        form.instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))


class LoginView(RegisterLoginPagesMixin,FormView):
    template_name = 'authentication/login.html'
    form_class = MyLoginForm
    success_url = reverse_lazy('budget:home-user')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pword = form.cleaned_data['password']
        usr = authenticate(username=uname,password=pword)
        if usr is not None and usr.owner:
            login(self.request,usr)
        else:
            return render(self.request,self.template_name,{'form':self.form_class,'error':'invalid credentials'})
        return super().form_valid(form)

    def get_next_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url



class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('budget:home-guest')

class  HomeGuest(RegisterLoginPagesMixin,TemplateView):
    template_name = 'home-guest.html'

class DebtView(LoginRequiredMixin,TemplateView):
    template_name = 'budget:widgets.html'


class AllTables(FetchData,TemplateView):
    template_name = 'tables.html'
    model = Income

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.request.user.owner
        household_cat = Expenses.objects.filter(category=1).filter(owner=owner)
        food_cat = Expenses.objects.filter(category=2).filter(owner=owner)
        transportation_cat = Expenses.objects.filter(category=3).filter(owner=owner)
        personal_cat = Expenses.objects.filter(category=4).filter(owner=owner)
        subscriptions_cat = Expenses.objects.filter(category=5).filter(owner=owner)
        savings_cat = Expenses.objects.filter(category=6).filter(owner=owner)
        medical_cat = Expenses.objects.filter(category=7).filter(owner=owner)
        context['household_cat'] = household_cat
        context['food_cat'] = food_cat
        context['transportation_cat'] = transportation_cat
        context['personal_cat'] = personal_cat
        context['subscriptions_cat'] = subscriptions_cat
        context['savings_cat'] = savings_cat
        context['medical_cat'] = medical_cat
        return context

class WidgetView(TemplateView):
    template_name = 'widgets.html'
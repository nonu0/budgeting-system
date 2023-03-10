from django import forms
from django.forms import  ModelForm
from .models import Owner,Income,Debt,Expenses,UserProfile
from django.contrib.auth.models import User
from .validators import password_validation

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=30,widget=forms.PasswordInput(),validators=[password_validation])
    password2 = forms.CharField(max_length=30,widget=forms.PasswordInput())
    class Meta:
        model = Owner
        fields = ['first_name','last_name','username','email','gender','phone_no','code','address','county','town']

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Username already exists')
        return uname

class MyLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



class IncomeForm(MultipleForm,forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source','planned_amount','actual_amount']

class DebtForm(MultipleForm,forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['paid_to','planned_amount','actual_amount']

class ExpenseForm(MultipleForm,forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['category','name_of_expense','planned_amount','actual_amount']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name','last_name','username','email','gender','town','county','phone_no','address','code']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
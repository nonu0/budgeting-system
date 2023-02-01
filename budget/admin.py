from django.contrib import admin
from .models import Owner,Income,Expenses,Debt,UserProfile

# Register your models here.

admin.site.register([Owner,Income,Expenses,Debt,UserProfile])
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db import models
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin



class GetObjectMixin(object):
    template_name = None
    form_class = None
    success_url = None
    objs = []
    def form_valid(self, form):
        print('working')
        for obj in self.objs:
            obj = form.cleaned_data.get('obj')
            form.instance.owner = self.request.user.owner
            print(form.instance.owner)
            form.instance.save()
        # messages.success(self.request,'Debt added successfully')
        return super().form_valid(form)
    

class FetchData(object):
    model = None
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        owner = self.request.user.owner
        # context['owner'] = owner
        model_objs = self.model.objects.filter(owner=owner)
        context['model_objs'] = model_objs
        return context




# class UserAccessMixin(PermissionRequiredMixin):


class RegisterLoginPagesMixin(object):
    template_name = None
    form_class = None
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            print('user is authenticated')
            return redirect('budget:home-user')
        return super().dispatch(request,*args,**kwargs)
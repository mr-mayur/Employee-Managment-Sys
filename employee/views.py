from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .forms import UserForm
from .models import *
from django.contrib.auth.decorators import login_required
from .decoretors import role_required, admin_only
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group


@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context ={}
    context['users'] = User.objects.all()
    context['title']= 'Employee'
    return render(request,'employee/index.html',context)


@login_required(login_url="/login/")
def employee_details(request, id=None):
    context ={}
    context['user'] = get_object_or_404(User, id=id)
    return render(request,'employee/details.html', context)

@login_required(login_url="/login/")
#@admin_only
@role_required
def employee_add(request):
    context={}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/add.html',context)
    else:
        user_form = UserForm()
        #context['user_form'] = user_form
        return render(request,'employee/add.html',{'user_form':user_form})

@login_required(login_url="/login/")
def employee_edit(request, id= None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/edit.html',{'user_form':user_form})
    else:
        user_form = UserForm(instance=user)
        #context['user_form'] = user_form
        return render(request,'employee/edit.html',{'user_form':user_form})

@login_required(login_url="/login/")
def employee_delete(request, id= None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html' ,context)

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary',]
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile


class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile

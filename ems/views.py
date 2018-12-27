from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required


def user_login(request):
    context ={}
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context ["error"] = "Provide valid credentials.."
            return render(request, "auth/login.html", context)

    else:
        return render(request,"auth/login.html",context)

@login_required(login_url="/login/")
def success(request):
    context ={}
    context['user'] = request.user
    return render(request, "auth/success.html", context)


def user_logout(request):
    if request.method =="POST":
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))



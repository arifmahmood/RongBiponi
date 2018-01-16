from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response


# Create your views here.
from django.template.context_processors import csrf


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/login')

def showHomePage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('home.html', c)

def showLoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')

    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def authenticationMethod(request):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    value = request.POST.get('userType')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)

        if value == 'admin':
            return HttpResponseRedirect("/admin")
        elif value == 'user':
            return HttpResponseRedirect("/home")

    elif user is None:
        c = {}
        c.update(csrf(request))
        return HttpResponseRedirect("/login")


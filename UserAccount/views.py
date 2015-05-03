from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


def is_username_exist(username):
    if User.objects.filter(username=username).count():
        return True
    return False
 
def signup(request):
    if request.method == "GET":
        return render(request,'UserAccount/register.html')
    elif request.method == "POST":
        print is_username_exist(request.POST.get('username'))
        if not(is_username_exist(request.POST.get('username'))):
            User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password'))
            messages.add_message(request, messages.INFO, 'Account Created. Please Login')
            return HttpResponseRedirect(reverse('user:login'))
        else:
            messages.add_message(request, messages.INFO, 'User Already exists. Please use different UserName')
            return HttpResponseRedirect(reverse('user:signup'))
 
def login(request):
    if request.user.is_authenticated():
     return HttpResponseRedirect(reverse('todo:home')) 
    elif request.method == "GET":
        return render(request,'UserAccount/login.html')
    elif request.method=="POST":
        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('todo:home'))
        else:
            messages.add_message(request, messages.INFO, 'Username or Password is incorrect')
            return HttpResponseRedirect(reverse('user:login'))

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect(reverse('user:login'))

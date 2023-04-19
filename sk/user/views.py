from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from django.urls import reverse 

def index(request):
    return render(request, "user/base.html")

def home(request):
    return render(request, "user/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (" Registration Successful! "))
    else:
        form= RegisterUserForm()
    return render(request, 'user/register.html', {'form':form })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect(reverse('user:home'))
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect(reverse('user:login'))
    else: 
        return render(request, 'user/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out! "))
    return redirect(reverse('user:index'))
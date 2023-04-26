from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from django.urls import reverse 
from .models import Profile, User
from recipe.models import Recipe

def index(request):
    return render(request, "user/about.html")

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (" Registration Successful! Welcome To The SocialKitchen Please Login."))
            return redirect(reverse('user:login'))
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
            messages.success(request, "Welcome Back!")
            return redirect(reverse('recipe:home'))
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect(reverse('user:login'))
    else: 
        return render(request, 'user/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out! "))
    return redirect(reverse('user:index'))

def profile_list(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        profiles = Profile.objects.exclude(user= request.user)
        return render(request, "user/profile_list.html", {'profiles':profiles})
    
def profile(request, id):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        user = User.objects.get(id=id)
        user_profile = Profile.objects.get(user= user)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follow.remove(user_profile)
            else:
                current_user_profile.follow.add(user_profile)
            current_user_profile.save()
        recipes = Recipe.objects.filter(user= user)
        return render(request, "user/profile.html", {'profile':user_profile, 'recipes':recipes})
    

def search_profile(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        matched_result = []
        if request.method == 'POST':
            search_query = request.POST.get('search')
            profiles = Profile.objects.exclude(user=request.user)
            for profile in profiles:
                if search_query == profile.user.username:
                    matched_result.append(profile)
                    break
                else:
                    if search_query.lower() in profile.user.username.lower():
                        matched_result.append(profile)

        return render(request, "user/search_profile.html", {'result':matched_result})



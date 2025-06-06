from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        
        user = UserProfile.objects.create_user(username=username, password=password, role=role)
        login(request, user)
        return redirect('profile')

    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'users/login.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('login')


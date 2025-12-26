from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

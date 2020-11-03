from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def account_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials")
        else:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect(reverse('dashboard'))
    return render(request, "account/login.html")


def dashboard(request):
    context = {}
    return render(request, "account/dashboard.html", context)

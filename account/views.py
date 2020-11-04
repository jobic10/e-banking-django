from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
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


@login_required
def account_dashboard(request):
    context = {}
    return render(request, "account/dashboard.html", context)


def account_logout(request):
    logout(request)
    messages.success(request, 'Thanks for the time!')
    return redirect(reverse('account_login'))

from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_login, name='account-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_login, name='account-login'),
    path('dashboard/', views.account_dashboard, name='dashboard'),
    path('logout/', views.account_logout, name='logout'),
]

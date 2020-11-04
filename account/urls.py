from django.urls import path
from . import views, staff_views

urlpatterns = [
    path('', views.account_login, name='account_login'),
    path('dashboard/', views.account_dashboard, name='dashboard'),
    path('logout/', views.account_logout, name='logout'),
    path('create_customer_account', staff_views.create_customer_account,
         name='create_customer_account'),
    path('view_customer/<int:customer_id>/',
         staff_views.view_customer, name='view_customer'),
]

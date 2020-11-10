from django.urls import path
from . import views, staff_views

urlpatterns = [
    path('', views.account_login, name='account_login'),
    path('dashboard/', views.account_dashboard, name='dashboard'),
    path('logout/', views.account_logout, name='logout'),
    path('create_customer_account/', staff_views.create_customer_account,
         name='create_customer_account'),
    path('view_customer/<int:customer_id>/',
         staff_views.view_customer, name='view_customer'),
    path("manage_customer/", staff_views.manage_all_customer,
         name='manage_all_customer'),
    path("manage_customer/savings/", staff_views.manage_savings_customer,
         name='manage_savings_customer'),
    path("manage_customer/current/", staff_views.manage_current_customer,
         name='manage_current_customer'),
    path("edit_customer/<int:customer_id>/",
         staff_views.edit_customer, name='edit_customer'),
    path("search/", staff_views.search_customer, name='search_customer'),
]

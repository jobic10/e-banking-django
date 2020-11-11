from django.urls import path
from . import views

urlpatterns = [
    path('<int:customer_id>/', views.start_transaction, name='start_transaction'),
    path('history/', views.transaction_logs, name='transaction_logs'),
    path('credit/', views.credit_transaction, name='credit_transaction'),
    path('debit/', views.debit_transaction, name='debit_transaction'),
]

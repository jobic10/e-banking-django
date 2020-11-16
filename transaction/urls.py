from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.transaction_logs, name='transaction_logs'),
    path('credit/', views.credit_transaction, name='credit_transaction'),
    path('view/<int:customer_id>/',
         views.view_transaction, name='view_transaction'),
    path('debit/', views.debit_transaction, name='debit_transaction'),
    path('transfer/', views.debit_transaction, name='transfer_transaction'),
    path('verify/<int:transaction_id>/',
         views.verify_transaction, name='verify_transaction'),
]

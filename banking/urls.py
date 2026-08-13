from django.urls import path
from . import views

urlpatterns = [
    path('', views.bank_list, name='bank_list'),
    path('account/add/', views.account_create, name='account_create'),
    path('account/<int:pk>/edit/', views.account_update, name='account_update'),
    path('account/<int:pk>/delete/', views.account_delete, name='account_delete'),
    path('transaction/add/', views.transaction_create, name='transaction_create'),
]

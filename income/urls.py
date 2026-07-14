from django.urls import path
from . import views

urlpatterns = [
    path('', views.income_list, name='income_list'),
    path('add/', views.income_create, name='income_create'),
    path('edit/<int:pk>/', views.income_update, name='income_update'),
    path('delete/<int:pk>/', views.income_delete, name='income_delete'),
]

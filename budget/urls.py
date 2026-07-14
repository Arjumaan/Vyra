from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_list, name='budget_list'),
    path('set/', views.budget_create, name='budget_create'),
    path('edit/<int:pk>/', views.budget_update, name='budget_update'),
    path('delete/<int:pk>/', views.budget_delete, name='budget_delete'),
]

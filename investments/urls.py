from django.urls import path
from . import views
urlpatterns = [
    path('', views.investment_list, name='investment_list'),
    path('add/', views.investment_create, name='investment_create'),
    path('<int:pk>/edit/', views.investment_update, name='investment_update'),
    path('<int:pk>/delete/', views.investment_delete, name='investment_delete'),
]

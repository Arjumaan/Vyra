from django.urls import path
from . import views

urlpatterns = [
    path('', views.debt_dashboard, name='debt_dashboard'),
]

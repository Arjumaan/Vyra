from django.urls import path
from . import views

urlpatterns = [
    path('', views.fire_dashboard, name='fire_dashboard'),
]

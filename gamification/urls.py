from django.urls import path
from . import views

urlpatterns = [
    path('', views.gamification_view, name='gamification_view'),
]

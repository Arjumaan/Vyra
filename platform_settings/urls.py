from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings_view, name='settings_view'),
    path('notifications/', views.notifications_view, name='notifications_view'),
]

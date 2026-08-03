from django.urls import path
from . import views

urlpatterns = [
    path('', views.security_center, name='security_center'),
    path('trigger/', views.trigger_backup, name='trigger_backup'),
]

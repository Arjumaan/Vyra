from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='real_estate_dashboard'),
    path('delete/<int:pk>/', views.delete_property, name='delete_property'),
]

from django.urls import path
from . import views
urlpatterns = [
    path('', views.bill_list, name='bill_list'),
    path('add/', views.bill_create, name='bill_create'),
    path('<int:pk>/edit/', views.bill_update, name='bill_update'),
    path('<int:pk>/delete/', views.bill_delete, name='bill_delete'),
    path('<int:pk>/toggle/', views.bill_toggle_paid, name='bill_toggle_paid'),
]

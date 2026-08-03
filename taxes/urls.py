from django.urls import path
from . import views

urlpatterns = [
    path('', views.tax_list, name='tax_list'),
    path('add/', views.tax_add, name='tax_add'),
    path('<int:pk>/edit/', views.tax_edit, name='tax_edit'),
    path('<int:pk>/delete/', views.tax_delete, name='tax_delete'),
    path('donation/add/', views.donation_add, name='donation_add'),
]

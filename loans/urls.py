from django.urls import path
from . import views
urlpatterns = [
    path('', views.loan_list, name='loan_list'),
    path('add/', views.loan_create, name='loan_create'),
    path('<int:pk>/edit/', views.loan_update, name='loan_update'),
    path('<int:pk>/delete/', views.loan_delete, name='loan_delete'),
]

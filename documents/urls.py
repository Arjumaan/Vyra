from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('add/', views.document_add, name='document_add'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
]

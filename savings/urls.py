from django.urls import path
from . import views
urlpatterns = [
    path('', views.savings_list, name='savings_list'),
    path('add/', views.savings_create, name='savings_create'),
    path('<int:pk>/', views.savings_detail, name='savings_detail'),
    path('<int:pk>/edit/', views.savings_update, name='savings_update'),
    path('<int:pk>/delete/', views.savings_delete, name='savings_delete'),
]

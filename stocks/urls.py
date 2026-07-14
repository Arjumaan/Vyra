from django.urls import path
from . import views
urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('add/', views.stock_create, name='stock_create'),
    path('<int:pk>/edit/', views.stock_update, name='stock_update'),
    path('<int:pk>/delete/', views.stock_delete, name='stock_delete'),
]

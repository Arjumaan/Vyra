from django.urls import path
from . import views
urlpatterns = [
    path('', views.crypto_list, name='crypto_list'),
    path('add/', views.crypto_create, name='crypto_create'),
    path('<int:pk>/edit/', views.crypto_update, name='crypto_update'),
    path('<int:pk>/delete/', views.crypto_delete, name='crypto_delete'),
]

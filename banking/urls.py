from django.urls import path
from . import views
urlpatterns = [
    path('', views.bank_list, name='bank_list'),
    path('bank/add/', views.bank_create, name='bank_create'),
    path('bank/<int:pk>/edit/', views.bank_update, name='bank_update'),
    path('bank/<int:pk>/delete/', views.bank_delete, name='bank_delete'),
    path('card/add/', views.card_create, name='card_create'),
    path('card/<int:pk>/edit/', views.card_update, name='card_update'),
    path('card/<int:pk>/delete/', views.card_delete, name='card_delete'),
]

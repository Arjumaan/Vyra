from django.urls import path
from . import views
urlpatterns = [
    path('', views.financial_hub, name='financial_hub'),
    path('networth/', views.net_worth, name='net_worth'),
    path('advisor/', views.ai_advisor, name='ai_advisor'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.financial_hub, name='financial_hub'),
    path('networth/', views.net_worth, name='net_worth'),
    path('advisor/', views.ai_advisor, name='ai_advisor'),
    path('assets/', views.AssetListView.as_view(), name='asset_list'),
    path('assets/add/', views.AssetCreateView.as_view(), name='asset_create'),
    path('assets/<int:pk>/edit/', views.AssetUpdateView.as_view(), name='asset_update'),
    path('assets/<int:pk>/delete/', views.AssetDeleteView.as_view(), name='asset_delete'),
]

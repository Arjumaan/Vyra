from django.urls import path
from . import views
urlpatterns = [
    path('', views.goal_list, name='goal_list'),
    path('add/', views.goal_create, name='goal_create'),
    path('<int:pk>/edit/', views.goal_update, name='goal_update'),
    path('<int:pk>/delete/', views.goal_delete, name='goal_delete'),
]

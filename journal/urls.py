from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_list, name='journal_list'),
    path('add/', views.journal_add, name='journal_add'),
    path('wishlist/add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/<int:pk>/edit/', views.wishlist_edit, name='wishlist_edit'),
    path('wishlist/<int:pk>/delete/', views.wishlist_delete, name='wishlist_delete'),
]

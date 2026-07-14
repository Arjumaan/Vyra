"""
URL configuration for Vyra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', accounts_views.register, name='register'),
    # Expense Tracker
    path('income/', include('income.urls')),
    path('expenses/', include('expenses.urls')),
    path('budget/', include('budget.urls')),
    path('reports/', include('reports.urls')),
    path('insights/', include('insights.urls')),
    # Wealth Management
    path('wealth/', include('wealth.urls')),
    path('savings/', include('savings.urls')),
    path('investments/', include('investments.urls')),
    path('stocks/', include('stocks.urls')),
    path('crypto/', include('crypto.urls')),
    path('banking/', include('banking.urls')),
    path('loans/', include('loans.urls')),
    path('insurance/', include('insurance.urls')),
    path('bills/', include('bills.urls')),
    path('goals/', include('goals.urls')),
]

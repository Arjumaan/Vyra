from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_budget', 'month', 'year')
    search_fields = ('user__username',)
    list_filter = ('year', 'month')

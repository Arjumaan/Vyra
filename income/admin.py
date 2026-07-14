from django.contrib import admin
from .models import Income

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'source', 'date')
    search_fields = ('source', 'user__username')
    list_filter = ('date', 'source')

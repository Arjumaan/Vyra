from django.contrib import admin
from .models import Account, BankTransaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('provider', 'nickname', 'category', 'account_type', 'current_balance', 'status', 'user')
    list_filter = ('category', 'account_type', 'status')
    search_fields = ('provider', 'nickname', 'account_number', 'user__username')

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'date', 'user')
    list_filter = ('transaction_type', 'date')
    search_fields = ('description', 'account__provider', 'user__username')

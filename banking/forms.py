from django import forms
from .models import Account, BankTransaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'category', 'account_type', 'provider', 'nickname', 'account_number',
            'currency', 'status', 'opening_balance', 'credit_limit', 'expiry_date',
            'rewards_program', 'notes', 'custom_icon', 'theme_color',
            'interest_rate', 'interest_type', 'compounding_frequency',
            'interest_credit_frequency', 'effective_date', 'maturity_date', 'tax_deduction'
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'maturity_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class BankTransactionForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = ['account', 'transaction_type', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

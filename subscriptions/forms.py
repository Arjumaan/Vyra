from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['service_name', 'plan_name', 'billing_cycle', 'amount', 'currency', 'start_date', 'next_billing_date', 'auto_renew', 'status', 'notes']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'neu-input'}),
            'plan_name': forms.TextInput(attrs={'class': 'neu-input'}),
            'billing_cycle': forms.Select(attrs={'class': 'neu-input'}),
            'amount': forms.NumberInput(attrs={'class': 'neu-input'}),
            'currency': forms.Select(attrs={'class': 'neu-input'}),
            'start_date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'next_billing_date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'auto_renew': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'neu-input'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 2}),
        }

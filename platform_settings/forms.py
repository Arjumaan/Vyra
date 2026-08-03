from django import forms
from .models import UserSettings

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['theme', 'base_currency', 'email_notifications', 'push_notifications', 'budget_alerts', 'bill_reminders', 'investment_alerts', 'security_alerts', 'hide_balances_by_default']
        widgets = {
            'theme': forms.Select(attrs={'class': 'neu-input'}),
            'base_currency': forms.Select(attrs={'class': 'neu-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'budget_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bill_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'investment_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'security_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hide_balances_by_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

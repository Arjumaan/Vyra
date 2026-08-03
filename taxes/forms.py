from django import forms
from .models import TaxRecord, Donation

class TaxRecordForm(forms.ModelForm):
    class Meta:
        model = TaxRecord
        fields = ['tax_year', 'tax_type', 'amount_due', 'amount_paid', 'currency', 'due_date', 'status', 'filing_receipt_number', 'notes']
        widgets = {
            'tax_year': forms.TextInput(attrs={'class': 'neu-input'}),
            'tax_type': forms.Select(attrs={'class': 'neu-input'}),
            'amount_due': forms.NumberInput(attrs={'class': 'neu-input'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'neu-input'}),
            'currency': forms.Select(attrs={'class': 'neu-input'}),
            'due_date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'neu-input'}),
            'filing_receipt_number': forms.TextInput(attrs={'class': 'neu-input'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 2}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['organization_name', 'amount', 'currency', 'date', 'is_tax_deductible', 'receipt_number', 'notes']
        widgets = {
            'organization_name': forms.TextInput(attrs={'class': 'neu-input'}),
            'amount': forms.NumberInput(attrs={'class': 'neu-input'}),
            'currency': forms.Select(attrs={'class': 'neu-input'}),
            'date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'is_tax_deductible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'receipt_number': forms.TextInput(attrs={'class': 'neu-input'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 2}),
        }

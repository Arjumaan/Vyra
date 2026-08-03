from django import forms
from .models import Asset, AssetCategory

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['category', 'name', 'currency', 'purchase_value', 'current_value', 'purchase_date', 'location_or_details']
        widgets = {
            'category': forms.Select(attrs={'class': 'neu-input'}),
            'name': forms.TextInput(attrs={'class': 'neu-input', 'placeholder': 'e.g. Primary Residence'}),
            'currency': forms.Select(attrs={'class': 'neu-input'}),
            'purchase_value': forms.NumberInput(attrs={'class': 'neu-input'}),
            'current_value': forms.NumberInput(attrs={'class': 'neu-input'}),
            'purchase_date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'location_or_details': forms.Textarea(attrs={'class': 'neu-input', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a Category"
        self.fields['currency'].empty_label = "Select a Currency"

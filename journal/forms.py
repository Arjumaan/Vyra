from django import forms
from .models import JournalEntry, WishlistItem

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['date', 'mood_score', 'tags', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'mood_score': forms.NumberInput(attrs={'class': 'neu-input', 'min': 1, 'max': 10}),
            'tags': forms.TextInput(attrs={'class': 'neu-input', 'placeholder': 'e.g. mindful, impulse'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 4}),
        }

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['item_name', 'estimated_cost', 'priority', 'status', 'target_date', 'product_url', 'notes']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'neu-input'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'neu-input'}),
            'priority': forms.Select(attrs={'class': 'neu-input'}),
            'status': forms.Select(attrs={'class': 'neu-input'}),
            'target_date': forms.DateInput(attrs={'class': 'neu-input', 'type': 'date'}),
            'product_url': forms.URLInput(attrs={'class': 'neu-input'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 2}),
        }

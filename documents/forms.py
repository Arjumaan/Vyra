from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file_path', 'is_encrypted', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'neu-input', 'placeholder': 'e.g. PAN Card'}),
            'document_type': forms.Select(attrs={'class': 'neu-input'}),
            'file_path': forms.ClearableFileInput(attrs={'class': 'neu-input'}),
            'is_encrypted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'neu-input', 'rows': 3}),
        }

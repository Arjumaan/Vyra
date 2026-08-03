from django.db import models
from django.contrib.auth.models import User
from documents.storage import AES256Storage

class Document(models.Model):
    DOC_TYPES = [
        ('identity', 'Identity (PAN/Aadhar/SSN)'),
        ('passport', 'Passport'),
        ('property', 'Property Deed'),
        ('vehicle', 'Vehicle RC/Title'),
        ('tax', 'Tax Return'),
        ('insurance', 'Insurance Policy'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOC_TYPES, default='other')
    
    # Military Grade AES-256 encrypted storage
    file_path = models.FileField(upload_to='secure_documents/', storage=AES256Storage())
    
    is_encrypted = models.BooleanField(default=True, help_text="Indicates if the file is encrypted at rest")
    notes = models.TextField(blank=True, null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"

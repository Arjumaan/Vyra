from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document
from .forms import DocumentForm

@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Calculate vault stats
    total_docs = documents.count()
    encrypted_docs = documents.filter(is_encrypted=True).count()
    
    return render(request, 'documents/document_list.html', {
        'documents': documents,
        'total_docs': total_docs,
        'encrypted_docs': encrypted_docs,
    })

@login_required
def document_add(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, "Document securely added to your digital vault.")
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'Upload Document'})

@login_required
def document_delete(request, pk):
    from django.shortcuts import get_object_or_404
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, "Document permanently deleted.")
        return redirect('document_list')
    return render(request, 'documents/document_confirm_delete.html', {'doc': doc})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry, WishlistItem
from .forms import JournalEntryForm, WishlistItemForm

@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user)
    wishlist = WishlistItem.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'journal/journal_list.html', {
        'entries': entries,
        'wishlist': wishlist,
    })

@login_required
def journal_add(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Journal entry saved.")
            return redirect('journal_list')
    else:
        form = JournalEntryForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'New Journal Entry'})

@login_required
def wishlist_add(request):
    if request.method == 'POST':
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Item added to wishlist.")
            return redirect('journal_list')
    else:
        form = WishlistItemForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'Add to Wishlist'})

@login_required
def wishlist_edit(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WishlistItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Wishlist updated.")
            return redirect('journal_list')
    else:
        form = WishlistItemForm(instance=item)
    return render(request, '_generic_form.html', {'form': form, 'title': 'Edit Wishlist'})

@login_required
def wishlist_delete(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Wishlist item removed.")
        return redirect('journal_list')
    return render(request, 'journal/wishlist_confirm_delete.html', {'item': item})

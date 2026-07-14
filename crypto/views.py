from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CryptoHolding
from django import forms

class CryptoForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CryptoHolding
        fields = ['coin_name', 'coin_symbol', 'quantity', 'buy_price', 'current_price', 'purchase_date', 'notes']

@login_required
def crypto_list(request):
    holdings = CryptoHolding.objects.filter(user=request.user)
    total_invested = sum(h.invested_amount() for h in holdings)
    total_current = sum(h.current_value() for h in holdings)
    total_pl = total_current - total_invested
    labels = [h.coin_symbol for h in holdings]
    data = [h.current_value() for h in holdings]
    return render(request, 'crypto/crypto_list.html', {
        'holdings': holdings,
        'total_invested': round(total_invested, 2),
        'total_current': round(total_current, 2),
        'total_pl': round(total_pl, 2),
        'chart_labels': labels,
        'chart_data': data,
    })

@login_required
def crypto_create(request):
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Crypto holding added.')
            return redirect('crypto_list')
    else:
        form = CryptoForm()
    return render(request, 'crypto/crypto_form.html', {'form': form, 'title': 'Add Crypto Holding'})

@login_required
def crypto_update(request, pk):
    h = get_object_or_404(CryptoHolding, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CryptoForm(request.POST, instance=h)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crypto updated.')
            return redirect('crypto_list')
    else:
        form = CryptoForm(instance=h)
    return render(request, 'crypto/crypto_form.html', {'form': form, 'title': 'Edit Crypto'})

@login_required
def crypto_delete(request, pk):
    h = get_object_or_404(CryptoHolding, pk=pk, user=request.user)
    if request.method == 'POST':
        h.delete()
        messages.success(request, 'Crypto holding removed.')
    return redirect('crypto_list')

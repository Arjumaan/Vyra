from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, CreditCard
from django import forms

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number', 'account_type', 'branch', 'ifsc', 'current_balance', 'interest_rate']

class CreditCardForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CreditCard
        fields = ['bank', 'card_name', 'credit_limit', 'used_credit', 'due_amount', 'due_date', 'billing_cycle_day', 'minimum_due', 'annual_fee']

@login_required
def bank_list(request):
    banks = BankAccount.objects.filter(user=request.user)
    cards = CreditCard.objects.filter(user=request.user)
    total_bank = sum(float(b.current_balance) for b in banks)
    total_credit_used = sum(float(c.used_credit) for c in cards)
    total_credit_limit = sum(float(c.credit_limit) for c in cards)
    return render(request, 'banking/bank_list.html', {
        'banks': banks, 'cards': cards,
        'total_bank': total_bank,
        'total_credit_used': total_credit_used,
        'total_credit_limit': total_credit_limit,
    })

@login_required
def bank_create(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Bank account added.')
            return redirect('bank_list')
    else:
        form = BankAccountForm()
    return render(request, 'banking/bank_form.html', {'form': form, 'title': 'Add Bank Account'})

@login_required
def bank_update(request, pk):
    bank = get_object_or_404(BankAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account updated.')
            return redirect('bank_list')
    else:
        form = BankAccountForm(instance=bank)
    return render(request, 'banking/bank_form.html', {'form': form, 'title': 'Edit Bank Account'})

@login_required
def bank_delete(request, pk):
    bank = get_object_or_404(BankAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        bank.delete()
        messages.success(request, 'Bank account removed.')
    return redirect('bank_list')

@login_required
def card_create(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Credit card added.')
            return redirect('bank_list')
    else:
        form = CreditCardForm()
    return render(request, 'banking/card_form.html', {'form': form, 'title': 'Add Credit Card'})

@login_required
def card_update(request, pk):
    card = get_object_or_404(CreditCard, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CreditCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credit card updated.')
            return redirect('bank_list')
    else:
        form = CreditCardForm(instance=card)
    return render(request, 'banking/card_form.html', {'form': form, 'title': 'Edit Credit Card'})

@login_required
def card_delete(request, pk):
    card = get_object_or_404(CreditCard, pk=pk, user=request.user)
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Credit card removed.')
    return redirect('bank_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, BankTransaction
from .forms import AccountForm, BankTransactionForm
from django.db.models import Sum

@login_required
def bank_list(request):
    accounts = Account.objects.filter(user=request.user)
    banks = accounts.filter(category='bank')
    cards = accounts.filter(category='card')
    
    total_bank = sum(float(b.current_balance) for b in banks)
    total_credit_used = sum(float(c.get_outstanding_amount()) for c in cards)
    total_credit_limit = sum(float(c.credit_limit) for c in cards)
    
    return render(request, 'banking/dashboard.html', {
        'banks': banks,
        'cards': cards,
        'total_bank': total_bank,
        'total_credit_used': total_credit_used,
        'total_credit_limit': total_credit_limit,
        'total_accounts_linked': len(banks) + len(cards),
    })

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.current_balance = obj.opening_balance
            obj.save()
            messages.success(request, 'Account added successfully.')
            return redirect('bank_list')
    else:
        initial = {}
        category = request.GET.get('category')
        if category in ['bank', 'card']:
            initial['category'] = category
        form = AccountForm(initial=initial)
    return render(request, 'banking/account_form.html', {'form': form, 'title': 'Add Account'})

@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            account.update_balance() # In case opening_balance changed
            messages.success(request, 'Account updated successfully.')
            return redirect('bank_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'banking/account_form.html', {'form': form, 'title': 'Edit Account'})

@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account removed.')
    return redirect('bank_list')

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = BankTransactionForm(request.user, request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Transaction added.')
            return redirect('bank_list')
    else:
        form = BankTransactionForm(request.user)
    return render(request, 'banking/transaction_form.html', {'form': form, 'title': 'Add Transaction'})

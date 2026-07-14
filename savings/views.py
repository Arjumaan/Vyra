from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SavingsAccount, SavingsTransaction
from django import forms

class SavingsAccountForm(forms.ModelForm):
    goal_deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = SavingsAccount
        fields = ['account_name', 'bank', 'account_type', 'current_balance', 'interest_rate',
                  'monthly_contribution', 'goal_amount', 'goal_deadline', 'notes']

class SavingsTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = SavingsTransaction
        fields = ['transaction_type', 'amount', 'date', 'notes']

@login_required
def savings_list(request):
    accounts = SavingsAccount.objects.filter(user=request.user)
    total_savings = sum(float(a.current_balance) for a in accounts)
    return render(request, 'savings/savings_list.html', {'accounts': accounts, 'total_savings': total_savings})

@login_required
def savings_create(request):
    if request.method == 'POST':
        form = SavingsAccountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Savings account created.')
            return redirect('savings_list')
    else:
        form = SavingsAccountForm()
    return render(request, 'savings/savings_form.html', {'form': form, 'title': 'Add Savings Account'})

@login_required
def savings_detail(request, pk):
    account = get_object_or_404(SavingsAccount, pk=pk, user=request.user)
    transactions = account.transactions.order_by('-date')
    if request.method == 'POST':
        form = SavingsTransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.account = account
            txn.save()
            # Update balance
            if txn.transaction_type == 'deposit':
                account.current_balance += txn.amount
            else:
                account.current_balance -= txn.amount
            account.save()
            messages.success(request, 'Transaction recorded.')
            return redirect('savings_detail', pk=pk)
    else:
        form = SavingsTransactionForm()
    return render(request, 'savings/savings_detail.html', {'account': account, 'transactions': transactions, 'form': form})

@login_required
def savings_update(request, pk):
    account = get_object_or_404(SavingsAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated.')
            return redirect('savings_list')
    else:
        form = SavingsAccountForm(instance=account)
    return render(request, 'savings/savings_form.html', {'form': form, 'title': 'Edit Account'})

@login_required
def savings_delete(request, pk):
    account = get_object_or_404(SavingsAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted.')
        return redirect('savings_list')
    return redirect('savings_list')

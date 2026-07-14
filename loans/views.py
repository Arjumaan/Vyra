from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan
from django import forms

class LoanForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = Loan
        fields = ['loan_name', 'loan_type', 'lender', 'loan_amount', 'outstanding_balance',
                  'interest_rate', 'emi_amount', 'emi_date', 'start_date', 'end_date', 'notes']

@login_required
def loan_list(request):
    loans = Loan.objects.filter(user=request.user)
    total_outstanding = sum(float(l.outstanding_balance) for l in loans)
    total_emi = sum(float(l.emi_amount) for l in loans)
    return render(request, 'loans/loan_list.html', {
        'loans': loans,
        'total_outstanding': round(total_outstanding, 2),
        'total_emi': round(total_emi, 2),
    })

@login_required
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Loan added.')
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'loans/loan_form.html', {'form': form, 'title': 'Add Loan'})

@login_required
def loan_update(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan updated.')
            return redirect('loan_list')
    else:
        form = LoanForm(instance=loan)
    return render(request, 'loans/loan_form.html', {'form': form, 'title': 'Edit Loan'})

@login_required
def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    if request.method == 'POST':
        loan.delete()
        messages.success(request, 'Loan removed.')
    return redirect('loan_list')

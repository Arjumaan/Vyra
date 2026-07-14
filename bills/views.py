from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bill
from django import forms
import datetime

class BillForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Bill
        fields = ['bill_name', 'category', 'amount', 'due_date', 'frequency', 'is_paid', 'auto_recurring', 'notes']

@login_required
def bill_list(request):
    bills = Bill.objects.filter(user=request.user).order_by('due_date')
    today = datetime.date.today()
    overdue = [b for b in bills if b.is_overdue()]
    upcoming = [b for b in bills if not b.is_paid and b.due_date >= today and (b.due_date - today).days <= 7]
    total_monthly = sum(float(b.amount) for b in bills if b.frequency == 'monthly')
    return render(request, 'bills/bill_list.html', {
        'bills': bills, 'overdue': overdue, 'upcoming': upcoming,
        'total_monthly': round(total_monthly, 2),
    })

@login_required
def bill_create(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Bill added.')
            return redirect('bill_list')
    else:
        form = BillForm()
    return render(request, 'bills/bill_form.html', {'form': form, 'title': 'Add Bill'})

@login_required
def bill_update(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated.')
            return redirect('bill_list')
    else:
        form = BillForm(instance=bill)
    return render(request, 'bills/bill_form.html', {'form': form, 'title': 'Edit Bill'})

@login_required
def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill removed.')
    return redirect('bill_list')

@login_required
def bill_toggle_paid(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    bill.is_paid = not bill.is_paid
    bill.save()
    return redirect('bill_list')

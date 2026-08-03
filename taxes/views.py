from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import TaxRecord, Donation
from .forms import TaxRecordForm, DonationForm

@login_required
def tax_list(request):
    taxes = TaxRecord.objects.filter(user=request.user).order_by('-tax_year', 'due_date')
    donations = Donation.objects.filter(user=request.user).order_by('-date')
    
    total_tax_paid = taxes.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_deductible_donations = donations.filter(is_tax_deductible=True).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'taxes/tax_list.html', {
        'taxes': taxes,
        'donations': donations,
        'total_tax_paid': total_tax_paid,
        'total_deductible_donations': total_deductible_donations,
    })

@login_required
def tax_add(request):
    if request.method == 'POST':
        form = TaxRecordForm(request.POST)
        if form.is_valid():
            tax = form.save(commit=False)
            tax.user = request.user
            tax.save()
            messages.success(request, "Tax record added.")
            return redirect('tax_list')
    else:
        form = TaxRecordForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'Add Tax Record'})

@login_required
def tax_edit(request, pk):
    tax = get_object_or_404(TaxRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaxRecordForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            messages.success(request, "Tax record updated.")
            return redirect('tax_list')
    else:
        form = TaxRecordForm(instance=tax)
    return render(request, '_generic_form.html', {'form': form, 'title': 'Edit Tax Record'})

@login_required
def tax_delete(request, pk):
    tax = get_object_or_404(TaxRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        tax.delete()
        messages.success(request, "Tax record removed.")
        return redirect('tax_list')
    return render(request, 'taxes/tax_confirm_delete.html', {'tax': tax})

@login_required
def donation_add(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.user = request.user
            don.save()
            messages.success(request, "Donation added.")
            return redirect('tax_list')
    else:
        form = DonationForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'Add Donation'})

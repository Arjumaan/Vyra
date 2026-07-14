from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Insurance
from django import forms

class InsuranceForm(forms.ModelForm):
    renewal_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Insurance
        fields = ['policy_name', 'insurance_type', 'provider', 'policy_number',
                  'premium_amount', 'premium_frequency', 'renewal_date',
                  'coverage_amount', 'nominee', 'notes']

@login_required
def insurance_list(request):
    policies = Insurance.objects.filter(user=request.user).order_by('renewal_date')
    total_premium = sum(float(p.premium_amount) for p in policies)
    return render(request, 'insurance/insurance_list.html', {
        'policies': policies,
        'total_premium': round(total_premium, 2),
    })

@login_required
def insurance_create(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Insurance policy added.')
            return redirect('insurance_list')
    else:
        form = InsuranceForm()
    return render(request, 'insurance/insurance_form.html', {'form': form, 'title': 'Add Policy'})

@login_required
def insurance_update(request, pk):
    policy = get_object_or_404(Insurance, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InsuranceForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Policy updated.')
            return redirect('insurance_list')
    else:
        form = InsuranceForm(instance=policy)
    return render(request, 'insurance/insurance_form.html', {'form': form, 'title': 'Edit Policy'})

@login_required
def insurance_delete(request, pk):
    policy = get_object_or_404(Insurance, pk=pk, user=request.user)
    if request.method == 'POST':
        policy.delete()
        messages.success(request, 'Policy removed.')
    return redirect('insurance_list')

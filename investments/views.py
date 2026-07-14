from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment
from django import forms

class InvestmentForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    maturity_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = Investment
        fields = ['investment_name', 'investment_type', 'invested_amount', 'current_value',
                  'purchase_date', 'broker', 'annual_return', 'maturity_date', 'notes']

@login_required
def investment_list(request):
    investments = Investment.objects.filter(user=request.user)
    total_invested = sum(float(i.invested_amount) for i in investments)
    total_current = sum(float(i.current_value) for i in investments)
    total_pl = total_current - total_invested
    # Group by type for chart
    type_totals = {}
    for inv in investments:
        t = inv.get_investment_type_display()
        type_totals[t] = type_totals.get(t, 0) + float(inv.current_value)
    return render(request, 'investments/investment_list.html', {
        'investments': investments,
        'total_invested': round(total_invested, 2),
        'total_current': round(total_current, 2),
        'total_pl': round(total_pl, 2),
        'chart_labels': list(type_totals.keys()),
        'chart_data': list(type_totals.values()),
    })

@login_required
def investment_create(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Investment added.')
            return redirect('investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investments/investment_form.html', {'form': form, 'title': 'Add Investment'})

@login_required
def investment_update(request, pk):
    inv = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=inv)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment updated.')
            return redirect('investment_list')
    else:
        form = InvestmentForm(instance=inv)
    return render(request, 'investments/investment_form.html', {'form': form, 'title': 'Edit Investment'})

@login_required
def investment_delete(request, pk):
    inv = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        inv.delete()
        messages.success(request, 'Investment deleted.')
    return redirect('investment_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BusinessProfile, BusinessTransaction
from decimal import Decimal
import datetime

@login_required
def dashboard(request):
    businesses = BusinessProfile.objects.filter(user=request.user)
    
    if request.method == 'POST' and 'create_business' in request.POST:
        name = request.POST.get('name')
        btype = request.POST.get('business_type')
        if name:
            BusinessProfile.objects.create(user=request.user, name=name, business_type=btype)
        return redirect('business_dashboard')
        
    if request.method == 'POST' and 'add_transaction' in request.POST:
        business_id = request.POST.get('business_id')
        t_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        date_str = request.POST.get('date') or datetime.date.today().isoformat()
        desc = request.POST.get('description')
        client = request.POST.get('client_or_vendor')
        is_deductible = request.POST.get('is_tax_deductible') == 'on'
        tax_category = request.POST.get('tax_category')
        
        bus = get_object_or_404(BusinessProfile, pk=business_id, user=request.user)
        BusinessTransaction.objects.create(
            business=bus,
            transaction_type=t_type,
            amount=Decimal(amount),
            date=date_str,
            description=desc,
            client_or_vendor=client,
            is_tax_deductible=is_deductible,
            tax_category=tax_category
        )
        return redirect('business_dashboard')

    overall_revenue = sum((b.total_revenue for b in businesses), Decimal('0'))
    overall_expenses = sum((b.total_expenses for b in businesses), Decimal('0'))
    overall_profit = sum((b.net_profit for b in businesses), Decimal('0'))
    overall_margin = (overall_profit / overall_revenue * Decimal('100')) if overall_revenue > 0 else Decimal('0')

    context = {
        'businesses': businesses,
        'overall_revenue': overall_revenue,
        'overall_expenses': overall_expenses,
        'overall_profit': overall_profit,
        'overall_margin': overall_margin,
    }
    return render(request, 'business_ledger/dashboard.html', context)

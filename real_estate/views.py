from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property
from decimal import Decimal

@login_required
def dashboard(request):
    properties = Property.objects.filter(user=request.user)
    
    # Portfolio calculations
    total_value = sum(p.current_value for p in properties) if properties else Decimal('0')
    total_equity = sum(p.equity for p in properties) if properties else Decimal('0')
    total_monthly_rent = sum(p.monthly_rental_income for p in properties) if properties else Decimal('0')
    total_monthly_cash_flow = sum(p.annual_cash_flow for p in properties) / Decimal('12') if properties else Decimal('0')
    
    # Compute overall cap rate and cash on cash
    overall_net_operating_income = sum(p.annual_net_operating_income for p in properties) if properties else Decimal('0')
    overall_cap_rate = (overall_net_operating_income / total_value * Decimal('100')) if total_value > 0 else Decimal('0')
    
    total_invested_cash = sum(p.down_payment for p in properties) if properties else Decimal('0')
    total_annual_cash_flow = sum(p.annual_cash_flow for p in properties) if properties else Decimal('0')
    overall_cash_on_cash = (total_annual_cash_flow / total_invested_cash * Decimal('100')) if total_invested_cash > 0 else Decimal('0')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        prop_type = request.POST.get('property_type')
        purchase_price = request.POST.get('purchase_price') or '0'
        current_value = request.POST.get('current_value') or '0'
        down_payment = request.POST.get('down_payment') or '0'
        rent = request.POST.get('rental_income') or '0'
        expenses = request.POST.get('operating_expenses') or '0'
        mortgage = request.POST.get('mortgage_balance') or '0'
        mortgage_payment = request.POST.get('mortgage_payment') or '0'
        
        Property.objects.create(
            user=request.user,
            name=name,
            property_type=prop_type,
            purchase_price=Decimal(purchase_price),
            current_value=Decimal(current_value),
            down_payment=Decimal(down_payment),
            monthly_rental_income=Decimal(rent),
            monthly_operating_expenses=Decimal(expenses),
            mortgage_balance=Decimal(mortgage),
            mortgage_monthly_payment=Decimal(mortgage_payment),
            has_mortgage=(Decimal(mortgage) > 0)
        )
        return redirect('real_estate_dashboard')

    context = {
        'properties': properties,
        'total_value': total_value,
        'total_equity': total_equity,
        'total_monthly_rent': total_monthly_rent,
        'total_monthly_cash_flow': total_monthly_cash_flow,
        'overall_cap_rate': overall_cap_rate,
        'overall_cash_on_cash': overall_cash_on_cash,
    }
    return render(request, 'real_estate/dashboard.html', context)

@login_required
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        prop.delete()
    return redirect('real_estate_dashboard')

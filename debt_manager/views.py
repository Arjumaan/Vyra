from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Debt, DebtStrategy
from .engine import DebtSimulator
from decimal import Decimal
import json

@login_required
def debt_dashboard(request):
    strategy, _ = DebtStrategy.objects.get_or_create(user=request.user)
    debts = Debt.objects.filter(user=request.user).order_by('-principal_balance')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_strategy':
            strategy.strategy_type = request.POST.get('strategy_type', 'avalanche')
            extra = request.POST.get('extra_payment')
            if extra:
                strategy.extra_monthly_payment = Decimal(extra)
            strategy.save()
            
        elif action == 'add_debt':
            Debt.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                principal_balance=Decimal(request.POST.get('balance')),
                interest_rate=Decimal(request.POST.get('rate')),
                minimum_payment=Decimal(request.POST.get('min_payment'))
            )
            
        elif action == 'delete_debt':
            debt_id = request.POST.get('debt_id')
            Debt.objects.filter(id=debt_id, user=request.user).delete()
            
        return redirect('debt_dashboard')

    simulator = DebtSimulator(debts, strategy)
    plan = simulator.get_plan()
    
    chart_data = None
    if plan:
        chart_data = json.dumps({
            'baseline': plan['baseline']['timeline'],
            'optimized': plan['optimized']['timeline']
        })
        
    context = {
        'debts': debts,
        'strategy': strategy,
        'plan': plan,
        'chart_data': chart_data
    }
    return render(request, 'debt_manager/dashboard.html', context)

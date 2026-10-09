from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FIREProfile
from .engine import FIRECalculator
from decimal import Decimal
from wealth.views import _get_wealth_data

@login_required
def fire_dashboard(request):
    profile, created = FIREProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.manual_annual_income = request.POST.get('income') or None
        profile.manual_annual_expenses = request.POST.get('expenses') or None
        profile.manual_current_net_worth = request.POST.get('net_worth') or None
        swr = request.POST.get('swr')
        if swr:
            profile.safe_withdrawal_rate = Decimal(swr)
        profile.save()
        return redirect('fire_dashboard')
        
    calc = FIRECalculator(profile)
    cache = calc.run_simulation()
    
    # Calculate Milestones for Tracker
    user_wealth_data = _get_wealth_data(request.user)
    real_net_worth = Decimal(str(user_wealth_data.get('net_worth', 0)))
    if real_net_worth <= Decimal('0'): real_net_worth = Decimal('100000.00')
    
    current_net_worth = profile.manual_current_net_worth or real_net_worth
    fire_number = cache.calculated_fire_number
    
    lean_fire = fire_number * Decimal('0.7')
    fat_fire = fire_number * Decimal('1.3')
    
    def get_progress(target):
        if target <= Decimal('0'): return 0
        return min(int((current_net_worth / target) * 100), 100)
        
    context = {
        'profile': profile,
        'cache': cache,
        'current_net_worth': current_net_worth,
        'lean_fire': lean_fire,
        'fat_fire': fat_fire,
        'lean_progress': get_progress(lean_fire),
        'standard_progress': get_progress(fire_number),
        'fat_progress': get_progress(fat_fire)
    }
    return render(request, 'fire_engine/dashboard.html', context)

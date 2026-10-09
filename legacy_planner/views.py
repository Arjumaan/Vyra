from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TrustedContact, Beneficiary, DeadMansSwitch
from decimal import Decimal
import django.utils.timezone as timezone

@login_required
def dashboard(request):
    contacts = TrustedContact.objects.filter(user=request.user)
    beneficiaries = Beneficiary.objects.filter(user=request.user)
    dms, _ = DeadMansSwitch.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'add_contact' in request.POST:
        TrustedContact.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            relationship=request.POST.get('relationship'),
            role=request.POST.get('role')
        )
        return redirect('legacy_dashboard')
        
    if request.method == 'POST' and 'add_beneficiary' in request.POST:
        Beneficiary.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            relationship=request.POST.get('relationship'),
            allocation_percentage=Decimal(request.POST.get('allocation_percentage') or '0'),
            notes=request.POST.get('notes')
        )
        return redirect('legacy_dashboard')

    if request.method == 'POST' and 'update_dms' in request.POST:
        dms.is_enabled = request.POST.get('is_enabled') == 'on'
        dms.check_in_frequency_days = int(request.POST.get('frequency') or 30)
        dms.grace_period_days = int(request.POST.get('grace') or 14)
        dms.save()
        return redirect('legacy_dashboard')

    if request.method == 'POST' and 'check_in' in request.POST:
        dms.last_check_in = timezone.now()
        dms.status = 'ACTIVE'
        dms.save()
        return redirect('legacy_dashboard')

    total_allocation = sum((b.allocation_percentage for b in beneficiaries), Decimal('0'))
    remaining_allocation = Decimal('100') - total_allocation

    context = {
        'contacts': contacts,
        'beneficiaries': beneficiaries,
        'dms': dms,
        'total_allocation': total_allocation,
        'remaining_allocation': remaining_allocation,
    }
    return render(request, 'legacy_planner/dashboard.html', context)

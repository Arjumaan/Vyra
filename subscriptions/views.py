from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Subscription
from .forms import SubscriptionForm

@login_required
def subscription_list(request):
    subs = Subscription.objects.filter(user=request.user)
    
    active_subs = subs.filter(status='active')
    monthly_spend = sum(sub.amount if sub.billing_cycle == 'monthly' else (sub.amount/12 if sub.billing_cycle == 'yearly' else sub.amount/3) for sub in active_subs)
    
    return render(request, 'subscriptions/subscription_list.html', {
        'subscriptions': subs,
        'monthly_spend': monthly_spend,
        'total_active': active_subs.count()
    })

@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, "Subscription tracked successfully.")
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, '_generic_form.html', {'form': form, 'title': 'Add Subscription'})

@login_required
def subscription_edit(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=sub)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription updated.")
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=sub)
    return render(request, '_generic_form.html', {'form': form, 'title': 'Edit Subscription'})

@login_required
def subscription_delete(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.delete()
        messages.success(request, "Subscription removed.")
        return redirect('subscription_list')
    return render(request, 'subscriptions/subscription_confirm_delete.html', {'sub': sub})

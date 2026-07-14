from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Budget
from .forms import BudgetForm

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    return render(request, 'budget/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            # Check if budget already exists for month/year
            if Budget.objects.filter(user=request.user, month=budget.month, year=budget.year).exists():
                messages.error(request, 'A budget already exists for this month and year.')
            else:
                budget.save()
                messages.success(request, 'Budget created successfully.')
                return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budget/budget_form.html', {'form': form, 'title': 'Set Monthly Budget'})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully.')
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budget/budget_form.html', {'form': form, 'title': 'Edit Budget'})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('budget_list')
    return redirect('budget_list')

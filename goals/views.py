from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal
from django import forms

class GoalForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = FinancialGoal
        fields = ['goal_name', 'goal_type', 'target_amount', 'current_amount', 'deadline', 'notes']

@login_required
def goal_list(request):
    goals = FinancialGoal.objects.filter(user=request.user).order_by('deadline')
    return render(request, 'goals/goal_list.html', {'goals': goals})

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Financial goal created.')
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form, 'title': 'Add Goal'})

@login_required
def goal_update(request, pk):
    goal = get_object_or_404(FinancialGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated.')
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form, 'title': 'Edit Goal'})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(FinancialGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal removed.')
    return redirect('goal_list')

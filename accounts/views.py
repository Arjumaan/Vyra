from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from income.models import Income
from expenses.models import Expense
from budget.models import Budget
from django.db.models import Sum
import datetime

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    today = datetime.date.today()
    
    # Calculate totals
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    
    # Current month budget
    budget = Budget.objects.filter(user=user, month=today.month, year=today.year).first()
    monthly_budget = budget.monthly_budget if budget else 0
    
    # Current month expenses
    monthly_expenses = Expense.objects.filter(user=user, date__month=today.month, date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0
    
    budget_usage = 0
    if monthly_budget > 0:
        budget_usage = (monthly_expenses / monthly_budget) * 100
        
    recent_activity = []
    incomes = Income.objects.filter(user=user).order_by('-date')[:5]
    expenses = Expense.objects.filter(user=user).order_by('-date')[:5]
    
    # Create simple activity list
    for inc in incomes:
        recent_activity.append({'type': 'income', 'amount': inc.amount, 'desc': inc.source, 'date': inc.date})
    for exp in expenses:
        recent_activity.append({'type': 'expense', 'amount': exp.amount, 'desc': exp.description or str(exp.category), 'date': exp.date})
        
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_activity[:5]
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'monthly_budget': monthly_budget,
        'monthly_expenses': monthly_expenses,
        'budget_usage': round(budget_usage, 2),
        'recent_activity': recent_activity
    }
    return render(request, 'dashboard.html', context)

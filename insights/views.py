from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expenses.models import Expense
from budget.models import Budget
from django.db.models import Sum
from datetime import datetime

@login_required
def insights_view(request):
    user = request.user
    today = datetime.now().date()
    
    # Current Month Data
    this_month_expenses = Expense.objects.filter(user=user, date__month=today.month, date__year=today.year)
    this_month_income = Income.objects.filter(user=user, date__month=today.month, date__year=today.year)
    budget = Budget.objects.filter(user=user, month=today.month, year=today.year).first()
    
    total_expense = this_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = this_month_income.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_budget = budget.monthly_budget if budget else 0
    
    insights = []
    
    if total_expense == 0 and total_income == 0:
        insights.append({
            'type': 'info',
            'icon': 'bi-info-circle',
            'text': "Welcome to Vyra! Start logging your transactions to get personalized financial insights."
        })
        return render(request, 'insights/insights.html', {'insights': insights})
    
    # Insight 1: Income vs Expense
    if total_expense > total_income > 0:
        insights.append({
            'type': 'danger',
            'icon': 'bi-exclamation-triangle',
            'text': f"Warning: Your expenses (₹{total_expense}) have exceeded your income (₹{total_income}) this month."
        })
    elif total_income > total_expense * 2:
        insights.append({
            'type': 'success',
            'icon': 'bi-check-circle',
            'text': "Excellent! You are maintaining healthy savings. Your income comfortably covers your monthly expenses."
        })
    
    # Insight 2: Budget Usage
    if monthly_budget > 0:
        usage = (total_expense / monthly_budget) * 100
        if usage > 100:
            insights.append({
                'type': 'danger',
                'icon': 'bi-exclamation-octagon',
                'text': f"Critical: You have exceeded your monthly budget by {usage - 100:.1f}%. Try to cut down unnecessary spending."
            })
        elif usage > 80:
            insights.append({
                'type': 'warning',
                'icon': 'bi-exclamation-circle',
                'text': f"Alert: You have used {usage:.1f}% of your budget. Only ₹{monthly_budget - total_expense} remaining."
            })
        elif usage < 50:
            insights.append({
                'type': 'success',
                'icon': 'bi-hand-thumbs-up',
                'text': f"Great job! You have only used {usage:.1f}% of your budget so far."
            })

    # Insight 3: Category Spending
    category_expenses = this_month_expenses.values('category__category_name').annotate(total=Sum('amount')).order_by('-total')
    if category_expenses:
        top_cat = category_expenses[0]
        cat_name = top_cat['category__category_name'] or 'Uncategorized'
        cat_total = top_cat['total']
        if total_expense > 0:
            cat_percent = (cat_total / total_expense) * 100
            if cat_percent > 30:
                insights.append({
                    'type': 'warning',
                    'icon': 'bi-pie-chart',
                    'text': f"You spent {cat_percent:.1f}% of your total expenses (₹{cat_total}) on {cat_name}. Consider reducing this to save more."
                })
            else:
                insights.append({
                    'type': 'info',
                    'icon': 'bi-pie-chart',
                    'text': f"Your highest expense category is {cat_name} at ₹{cat_total} ({cat_percent:.1f}% of total)."
                })
                
    # Insight 4: General Tips
    insights.append({
        'type': 'primary',
        'icon': 'bi-lightbulb',
        'text': "AI Tip: Try applying the 50/30/20 rule - 50% for needs, 30% for wants, and 20% for savings."
    })

    return render(request, 'insights/insights.html', {'insights': insights})

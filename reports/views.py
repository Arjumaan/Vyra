from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expenses.models import Expense
from django.db.models import Sum
from datetime import datetime, timedelta

@login_required
def reports_view(request):
    user = request.user
    today = datetime.now().date()
    
    # This Month
    this_month_expenses = Expense.objects.filter(user=user, date__month=today.month, date__year=today.year)
    this_month_income = Income.objects.filter(user=user, date__month=today.month, date__year=today.year)
    
    total_expense = this_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = this_month_income.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expense
    
    # Top spending category
    category_expenses = this_month_expenses.values('category__category_name').annotate(total=Sum('amount')).order_by('-total')
    top_category = category_expenses.first() if category_expenses else None
    
    # Highest/Lowest expense
    highest_expense = this_month_expenses.order_by('-amount').first()
    lowest_expense = this_month_expenses.order_by('amount').first()
    
    avg_daily = float(total_expense) / today.day if today.day > 0 else 0
    
    # Prepare chart data for categories
    chart_labels = [item['category__category_name'] or 'Uncategorized' for item in category_expenses]
    chart_data = [float(item['total']) for item in category_expenses]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'top_category': top_category,
        'highest_expense': highest_expense,
        'lowest_expense': lowest_expense,
        'avg_daily': round(avg_daily, 2),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'month_name': today.strftime('%B %Y')
    }
    return render(request, 'reports/reports.html', context)

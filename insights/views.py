from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expenses.models import Expense
from django.db.models import Sum, Count
import datetime
from dateutil.relativedelta import relativedelta
from wealth.views import _get_wealth_data

@login_required
def insights_view(request):
    user = request.user
    today = datetime.date.today()
    
    # Base wealth data for overview metrics
    wealth_data = _get_wealth_data(user)
    
    # 6-Month Cash Flow Analysis
    cashflow_labels = []
    cashflow_income = []
    cashflow_expense = []
    
    for i in range(5, -1, -1):
        target_date = today - relativedelta(months=i)
        month_name = target_date.strftime("%b %Y")
        
        inc = Income.objects.filter(user=user, date__month=target_date.month, date__year=target_date.year).aggregate(Sum('amount'))['amount__sum'] or 0
        exp = Expense.objects.filter(user=user, date__month=target_date.month, date__year=target_date.year).aggregate(Sum('amount'))['amount__sum'] or 0
        
        cashflow_labels.append(month_name)
        cashflow_income.append(float(inc))
        cashflow_expense.append(float(exp))
        
    # Current Month Category Heatmap
    this_month_expenses = Expense.objects.filter(user=user, date__month=today.month, date__year=today.year)
    category_expenses = this_month_expenses.values('category__category_name').annotate(total=Sum('amount')).order_by('-total')[:6]
    
    heatmap_labels = []
    heatmap_data = []
    for c in category_expenses:
        name = c['category__category_name'] or 'Uncategorized'
        heatmap_labels.append(name)
        heatmap_data.append(float(c['total']))
        
    # Frequent Expenses (Count based)
    frequent_expenses = this_month_expenses.values('description').annotate(count=Count('id'), total=Sum('amount')).order_by('-count')[:5]
    freq_list = []
    for f in frequent_expenses:
        if f['description']:
            freq_list.append({
                'name': f['description'],
                'count': f['count'],
                'total': float(f['total'])
            })
            
    # Key Metrics
    total_income_6m = sum(cashflow_income)
    total_expense_6m = sum(cashflow_expense)
    savings_rate_6m = 0
    if total_income_6m > 0:
        savings_rate_6m = ((total_income_6m - total_expense_6m) / total_income_6m) * 100

    context = {
        'net_worth': wealth_data['net_worth'],
        'health_score': wealth_data['health_score'],
        'cashflow_labels': cashflow_labels,
        'cashflow_income': cashflow_income,
        'cashflow_expense': cashflow_expense,
        'heatmap_labels': heatmap_labels,
        'heatmap_data': heatmap_data,
        'freq_list': freq_list,
        'total_income_6m': total_income_6m,
        'total_expense_6m': total_expense_6m,
        'savings_rate_6m': round(savings_rate_6m, 1)
    }
    
    return render(request, 'insights/insights.html', context)

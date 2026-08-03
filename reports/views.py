from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expenses.models import Expense
from django.db.models import Sum
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse

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

@login_required
def export_csv(request):
    user = request.user
    export_type = request.GET.get('type', 'transactions') # 'transactions', 'income', 'expenses'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="vyra_{export_type}_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    if export_type == 'income':
        writer.writerow(['Date', 'Source', 'Amount', 'Description'])
        incomes = Income.objects.filter(user=user).order_by('-date')
        for i in incomes:
            writer.writerow([i.date, i.source, i.amount, i.description])
            
    elif export_type == 'expenses':
        writer.writerow(['Date', 'Category', 'Amount', 'Description', 'Merchant'])
        expenses = Expense.objects.filter(user=user).order_by('-date')
        for e in expenses:
            category_name = e.category.category_name if e.category else 'Uncategorized'
            writer.writerow([e.date, category_name, e.amount, e.description, e.merchant])
            
    else: # Mixed Transactions
        writer.writerow(['Date', 'Type', 'Category/Source', 'Amount', 'Description'])
        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)
        
        transactions = []
        for i in incomes:
            transactions.append({'date': i.date, 'type': 'Income', 'cat': i.source, 'amt': i.amount, 'desc': i.description})
        for e in expenses:
            cat = e.category.category_name if e.category else 'Uncategorized'
            transactions.append({'date': e.date, 'type': 'Expense', 'cat': cat, 'amt': e.amount, 'desc': e.description})
            
        transactions.sort(key=lambda x: x['date'], reverse=True)
        for t in transactions:
            writer.writerow([t['date'], t['type'], t['cat'], t['amt'], t['desc']])
            
    return response

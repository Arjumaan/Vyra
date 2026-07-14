from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from savings.models import SavingsAccount
from investments.models import Investment
from stocks.models import Stock
from crypto.models import CryptoHolding
from banking.models import BankAccount, CreditCard
from loans.models import Loan
from insurance.models import Insurance
from bills.models import Bill
from goals.models import FinancialGoal
from income.models import Income
from expenses.models import Expense
from django.db.models import Sum
import datetime

def _get_wealth_data(user):
    today = datetime.date.today()
    # Assets
    bank_balance = BankAccount.objects.filter(user=user).aggregate(Sum('current_balance'))['current_balance__sum'] or 0
    savings_balance = SavingsAccount.objects.filter(user=user).aggregate(Sum('current_balance'))['current_balance__sum'] or 0
    investment_value = sum(float(i.current_value) for i in Investment.objects.filter(user=user))
    stock_value = sum(s.current_value() for s in Stock.objects.filter(user=user))
    crypto_value = sum(c.current_value() for c in CryptoHolding.objects.filter(user=user))
    total_assets = float(bank_balance) + float(savings_balance) + investment_value + stock_value + crypto_value

    # Liabilities
    total_loans = float(Loan.objects.filter(user=user).aggregate(Sum('outstanding_balance'))['outstanding_balance__sum'] or 0)
    total_credit_used = float(CreditCard.objects.filter(user=user).aggregate(Sum('used_credit'))['used_credit__sum'] or 0)
    total_liabilities = total_loans + total_credit_used

    net_worth = total_assets - total_liabilities

    # Monthly EMI
    monthly_emi = float(Loan.objects.filter(user=user).aggregate(Sum('emi_amount'))['emi_amount__sum'] or 0)

    # Emergency fund (savings accounts tagged as emergency)
    emergency_fund = float(SavingsAccount.objects.filter(user=user, account_type='emergency').aggregate(Sum('current_balance'))['current_balance__sum'] or 0)

    # Income & Expenses this month
    this_month_income = float(Income.objects.filter(user=user, date__month=today.month, date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0)
    this_month_expenses = float(Expense.objects.filter(user=user, date__month=today.month, date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0)

    # Financial Health Score (0–100)
    score = 50
    if net_worth > 0: score += 15
    if this_month_income > 0 and this_month_expenses / this_month_income < 0.7: score += 10
    if emergency_fund > this_month_expenses * 3: score += 10
    if total_credit_used > 0 and total_liabilities / max(total_assets, 1) < 0.4: score += 10
    if monthly_emi < this_month_income * 0.4: score += 5
    score = min(max(score, 0), 100)

    # Breakdowns for charts
    asset_labels = ['Bank Balance', 'Savings', 'Investments', 'Stocks', 'Crypto']
    asset_data = [float(bank_balance), float(savings_balance), investment_value, stock_value, crypto_value]

    liability_labels = ['Outstanding Loans', 'Credit Card Used']
    liability_data = [total_loans, total_credit_used]

    return {
        'net_worth': round(net_worth, 2),
        'total_assets': round(total_assets, 2),
        'total_liabilities': round(total_liabilities, 2),
        'bank_balance': round(float(bank_balance), 2),
        'savings_balance': round(float(savings_balance), 2),
        'investment_value': round(investment_value, 2),
        'stock_value': round(stock_value, 2),
        'crypto_value': round(crypto_value, 2),
        'total_loans': round(total_loans, 2),
        'total_credit_used': round(total_credit_used, 2),
        'monthly_emi': round(monthly_emi, 2),
        'emergency_fund': round(emergency_fund, 2),
        'health_score': score,
        'asset_labels': asset_labels,
        'asset_data': asset_data,
        'liability_labels': liability_labels,
        'liability_data': liability_data,
        'this_month_income': round(this_month_income, 2),
        'this_month_expenses': round(this_month_expenses, 2),
    }

@login_required
def financial_hub(request):
    data = _get_wealth_data(request.user)
    # Upcoming bills
    upcoming_bills = Bill.objects.filter(user=request.user, is_paid=False).order_by('due_date')[:5]
    # Active goals
    goals = FinancialGoal.objects.filter(user=request.user).order_by('deadline')[:3]
    data.update({'upcoming_bills': upcoming_bills, 'goals': goals})
    return render(request, 'wealth/financial_hub.html', data)

@login_required
def net_worth(request):
    data = _get_wealth_data(request.user)
    return render(request, 'wealth/net_worth.html', data)

@login_required
def ai_advisor(request):
    user = request.user
    data = _get_wealth_data(user)
    today = datetime.date.today()

    insights = []

    # Net worth insight
    if data['net_worth'] > 0:
        insights.append({'type': 'success', 'icon': 'bi-graph-up-arrow',
            'text': f"Your net worth is ₹{data['net_worth']:,.2f}. Keep growing your assets!"})
    else:
        insights.append({'type': 'danger', 'icon': 'bi-exclamation-triangle',
            'text': f"Your net worth is negative (₹{data['net_worth']:,.2f}). Focus on reducing liabilities."})

    # Emergency fund
    monthly_exp = data['this_month_expenses']
    if data['emergency_fund'] < monthly_exp * 3:
        insights.append({'type': 'warning', 'icon': 'bi-shield-exclamation',
            'text': f"Your emergency fund (₹{data['emergency_fund']:,.2f}) is below the recommended 3-6 months of expenses."})
    else:
        insights.append({'type': 'success', 'icon': 'bi-shield-check',
            'text': f"Great! Your emergency fund covers {int(data['emergency_fund'] / max(monthly_exp, 1))} months of expenses."})

    # Credit utilization
    credit_cards = CreditCard.objects.filter(user=user)
    if credit_cards.exists():
        total_limit = sum(float(c.credit_limit) for c in credit_cards)
        total_used = sum(float(c.used_credit) for c in credit_cards)
        util = (total_used / total_limit * 100) if total_limit > 0 else 0
        if util > 40:
            insights.append({'type': 'danger', 'icon': 'bi-credit-card',
                'text': f"Your credit utilization is {util:.1f}%. Keep it below 30% to maintain a healthy credit score."})
        else:
            insights.append({'type': 'success', 'icon': 'bi-credit-card',
                'text': f"Your credit utilization is {util:.1f}% — within a healthy range."})

    # EMI ratio
    if data['this_month_income'] > 0:
        emi_ratio = (data['monthly_emi'] / data['this_month_income']) * 100
        if emi_ratio > 40:
            insights.append({'type': 'warning', 'icon': 'bi-bank',
                'text': f"Your EMI-to-income ratio is {emi_ratio:.1f}%. Financial experts recommend keeping this below 40%."})

    # Investment allocation
    total_assets = data['total_assets']
    if total_assets > 0:
        inv_pct = (data['investment_value'] / total_assets) * 100
        if inv_pct < 20:
            insights.append({'type': 'info', 'icon': 'bi-pie-chart',
                'text': f"Only {inv_pct:.1f}% of your wealth is invested. Consider increasing investments for long-term growth."})
        if data['crypto_value'] / total_assets * 100 > 20:
            insights.append({'type': 'warning', 'icon': 'bi-currency-bitcoin',
                'text': "Crypto exceeds 20% of your portfolio. High volatility — consider diversification."})
        if data['bank_balance'] / total_assets * 100 > 60:
            insights.append({'type': 'info', 'icon': 'bi-cash-stack',
                'text': "You have significant idle cash in bank accounts. Consider investing for better returns."})

    # Health score
    if data['health_score'] >= 80:
        insights.append({'type': 'success', 'icon': 'bi-stars',
            'text': f"Excellent! Your Financial Health Score is {data['health_score']}/100. Keep up the great work!"})
    elif data['health_score'] >= 60:
        insights.append({'type': 'info', 'icon': 'bi-activity',
            'text': f"Your Financial Health Score is {data['health_score']}/100. There is room for improvement."})
    else:
        insights.append({'type': 'danger', 'icon': 'bi-heart-pulse',
            'text': f"Your Financial Health Score is {data['health_score']}/100. Focus on reducing debt and building savings."})

    # Upcoming bills
    overdue_bills = Bill.objects.filter(user=user, is_paid=False, due_date__lt=today).count()
    if overdue_bills > 0:
        insights.append({'type': 'danger', 'icon': 'bi-receipt',
            'text': f"You have {overdue_bills} overdue bill(s). Pay them immediately to avoid late fees."})

    data.update({'insights': insights})
    return render(request, 'wealth/ai_advisor.html', data)

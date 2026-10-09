from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from income.models import Income
from expenses.models import Expense
from wealth.models import Asset
from debt_manager.models import Debt
from real_estate.models import Property
from business_ledger.models import BusinessProfile
from fire_engine.models import FIREProfile
from legacy_planner.models import DeadMansSwitch

# New imports for full wealth connectivity
from savings.models import SavingsAccount
from investments.models import Investment
from stocks.models import Stock
from crypto.models import CryptoHolding
from banking.models import Account
from loans.models import Loan
from taxes.models import TaxRecord

@login_required
def dashboard(request):
    user = request.user
    
    # 1. Cashflow & Banking
    total_income = sum((i.amount for i in Income.objects.filter(user=user)), Decimal('0'))
    total_expenses = sum((e.amount for e in Expense.objects.filter(user=user)), Decimal('0'))
    liquid_cash = total_income - total_expenses
    
    bank_accounts = Account.objects.filter(user=user)
    bank_balance = sum((a.current_balance for a in bank_accounts), Decimal('0'))
    
    total_liquidity = liquid_cash + bank_balance
    
    # 2. Hard Assets (from wealth app)
    base_assets_value = sum((a.current_value for a in Asset.objects.filter(user=user)), Decimal('0'))
    
    # 3. Real Estate
    properties = Property.objects.filter(user=user)
    real_estate_equity = sum((p.equity for p in properties), Decimal('0'))
    
    # 4. Business
    businesses = BusinessProfile.objects.filter(user=user)
    business_profit = sum((b.net_profit for b in businesses), Decimal('0'))
    
    # 5. Investments & Markets (Savings, Investments, Stocks, Crypto)
    savings = sum((s.current_balance for s in SavingsAccount.objects.filter(user=user)), Decimal('0'))
    investments = sum((i.current_value for i in Investment.objects.filter(user=user)), Decimal('0'))
    stocks = sum(((s.quantity * s.current_price) for s in Stock.objects.filter(user=user)), Decimal('0'))
    crypto = sum(((c.quantity * c.current_price) for c in CryptoHolding.objects.filter(user=user)), Decimal('0'))
    
    market_portfolio_value = savings + investments + stocks + crypto
    
    # 6. Liabilities (Debt & Loans & Taxes)
    debts = Debt.objects.filter(user=user)
    base_debt = sum((d.principal_balance for d in debts), Decimal('0'))
    
    loans = Loan.objects.filter(user=user)
    total_loans = sum((l.outstanding_balance for l in loans), Decimal('0'))
    
    taxes = TaxRecord.objects.filter(user=user)
    tax_liabilities = sum(((t.amount_due - t.amount_paid) for t in taxes), Decimal('0'))
    
    total_debt = base_debt + total_loans + tax_liabilities
    
    # Master Net Worth Calculation
    total_assets = total_liquidity + base_assets_value + real_estate_equity + business_profit + market_portfolio_value
    net_worth = total_assets - total_debt
    
    # 7. FIRE Engine
    fire_profile = FIREProfile.objects.filter(user=user).first()
    
    # 8. Legacy
    dms = DeadMansSwitch.objects.filter(user=user).first()
    
    context = {
        'net_worth': net_worth,
        'liquid_cash': liquid_cash,
        'bank_balance': bank_balance,
        'total_liquidity': total_liquidity,
        'base_assets_value': base_assets_value,
        'real_estate_equity': real_estate_equity,
        'business_profit': business_profit,
        'market_portfolio_value': market_portfolio_value,
        'savings': savings,
        'investments': investments,
        'stocks': stocks,
        'crypto': crypto,
        'total_assets': total_assets,
        'total_debt': total_debt,
        'base_debt': base_debt,
        'total_loans': total_loans,
        'tax_liabilities': tax_liabilities,
        'fire_profile': fire_profile,
        'dms': dms,
    }
    return render(request, 'financial_hub/dashboard.html', context)

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_CATEGORIES = [
        ('bank', 'Bank Account'),
        ('card', 'Card'),
    ]

    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
        ('salary', 'Salary Account'),
        ('joint', 'Joint Account'),
        ('fixed_deposit', 'Fixed Deposit'),
        ('recurring_deposit', 'Recurring Deposit'),
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('prepaid', 'Prepaid Card'),
        ('virtual', 'Virtual Card'),
        ('forex', 'Forex Card'),
        ('utility', 'Utility / Stored Value Card'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banking_accounts')
    category = models.CharField(max_length=20, choices=ACCOUNT_CATEGORIES, default='bank')
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPES, default='savings')
    
    provider = models.CharField(max_length=150, help_text="Bank or Provider Name")
    nickname = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    interest_accrued = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    
    credit_limit = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True, default=0)
    
    expiry_date = models.DateField(blank=True, null=True)
    rewards_program = models.CharField(max_length=255, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)
    custom_icon = models.CharField(max_length=50, blank=True, null=True, help_text="Bootstrap icon class")
    theme_color = models.CharField(max_length=20, blank=True, null=True, help_text="Hex color code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    INTEREST_TYPES = [
        ('simple', 'Simple Interest'),
        ('compound', 'Compound Interest'),
    ]
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half-Yearly'),
        ('annually', 'Annually'),
        ('at_maturity', 'At Maturity'),
    ]
    
    interest_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    interest_type = models.CharField(max_length=20, choices=INTEREST_TYPES, default='simple')
    compounding_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True, null=True)
    interest_credit_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    maturity_date = models.DateField(blank=True, null=True)
    tax_deduction = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Tax withholding %")

    def __str__(self):
        return self.nickname or f"{self.provider} - {self.get_account_type_display()}"
        
    def get_outstanding_amount(self):
        if self.category == 'card' and self.credit_limit:
            if self.current_balance < 0:
                return abs(self.current_balance)
        return 0

    def get_available_balance(self):
        if self.category == 'card' and self.credit_limit:
            return float(self.credit_limit) + float(self.current_balance)
        return float(self.current_balance)

    def utilization_percent(self):
        if self.category == 'card' and self.credit_limit and self.credit_limit > 0:
            outstanding = self.get_outstanding_amount()
            return round((float(outstanding) / float(self.credit_limit)) * 100, 1)
        return 0

    def update_balance(self):
        transactions = self.transactions.all()
        bal = self.opening_balance
        for t in transactions:
            if t.transaction_type in ['income', 'adjustment_credit', 'interest', 'refund', 'cashback', 'rewards', 'salary', 'bonus', 'cash_deposit', 'investment_return']:
                bal += t.amount
            elif t.transaction_type in ['expense', 'adjustment_debit', 'fee', 'tax', 'purchase', 'bill', 'atm', 'emi', 'subscription', 'loan_repayment']:
                bal -= t.amount
            elif t.transaction_type in ['transfer', 'internal', 'wallet', 'upi', 'neft', 'rtgs', 'imps', 'wire']:
                bal += t.amount # amount can be negative for outgoing, positive for incoming
        self.current_balance = bal
        self.save()

    def calculate_accrued_interest(self, as_of_date=None):
        if self.interest_rate <= 0:
            return 0
        from django.utils import timezone
        if as_of_date is None:
            as_of_date = timezone.now().date()
        
        start_date = self.effective_date or self.created_at.date()
        if start_date > as_of_date:
            return 0
            
        days = (as_of_date - start_date).days
        rate = float(self.interest_rate) / 100.0
        principal = float(self.current_balance)
        
        if self.interest_type == 'simple':
            # Simple interest: P * R * T (in years)
            return principal * rate * (days / 365.25)
        elif self.interest_type == 'compound':
            # Compound interest
            n = 1
            if self.compounding_frequency == 'daily':
                n = 365
            elif self.compounding_frequency == 'monthly':
                n = 12
            elif self.compounding_frequency == 'quarterly':
                n = 4
            elif self.compounding_frequency == 'half_yearly':
                n = 2
            elif self.compounding_frequency == 'annually':
                n = 1
            
            t = days / 365.25
            amount = principal * ((1 + (rate / n)) ** (n * t))
            return amount - principal
        return 0



class BankTransaction(models.Model):
    TRANSACTION_TYPES = [
        # Income types
        ('income', 'Income'),
        ('salary', 'Salary'),
        ('bonus', 'Bonus'),
        ('cash_deposit', 'Cash Deposit'),
        ('interest', 'Interest Credit'),
        ('refund', 'Refund'),
        ('investment_return', 'Investment Return'),
        ('cashback', 'Cashback'),
        ('rewards', 'Rewards'),
        
        # Expense types
        ('expense', 'Expense'),
        ('purchase', 'Purchase'),
        ('bill', 'Bill Payment'),
        ('atm', 'ATM Withdrawal'),
        ('fee', 'Bank Charges'),
        ('emi', 'EMI'),
        ('tax', 'Taxes'),
        ('subscription', 'Subscription'),
        ('loan_repayment', 'Loan Repayment'),
        
        # Transfers
        ('transfer', 'Transfer'),
        ('internal', 'Internal Transfer'),
        ('wallet', 'Wallet Transfer'),
        ('upi', 'UPI'),
        ('neft', 'NEFT'),
        ('rtgs', 'RTGS'),
        ('imps', 'IMPS'),
        ('wire', 'Wire Transfer'),
        
        # Adjustments
        ('adjustment_credit', 'Balance Correction (Credit)'),
        ('adjustment_debit', 'Balance Correction (Debit)'),
        ('reversal', 'Reversal'),
        ('chargeback', 'Chargeback'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2) # Negative for outgoing, positive for incoming.
    date = models.DateTimeField()
    description = models.CharField(max_length=255)
    
    # For transfers
    related_transaction = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.account.update_balance()

    def delete(self, *args, **kwargs):
        account = self.account
        super().delete(*args, **kwargs)
        account.update_balance()

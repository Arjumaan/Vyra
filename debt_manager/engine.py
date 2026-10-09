from decimal import Decimal
import copy

class DebtSimulator:
    def __init__(self, debts, strategy):
        self.original_debts = [
            {
                'id': d.id,
                'name': d.name,
                'balance': d.principal_balance,
                'rate': d.interest_rate,
                'min_payment': d.minimum_payment
            } for d in debts
        ]
        self.strategy_type = strategy.strategy_type
        self.extra_payment = strategy.extra_monthly_payment
        
    def _run_simulation(self, strategy_type, extra_payment):
        # Clone debts
        current_debts = copy.deepcopy(self.original_debts)
        
        # Sort based on strategy
        if strategy_type == 'snowball':
            # Lowest balance first
            current_debts.sort(key=lambda x: x['balance'])
        elif strategy_type == 'avalanche':
            # Highest interest first
            current_debts.sort(key=lambda x: x['rate'], reverse=True)
            
        months = 0
        total_interest_paid = Decimal('0')
        timeline = []
        
        while any(d['balance'] > Decimal('0') for d in current_debts) and months < 1200:
            months += 1
            available_extra = extra_payment
            
            # Step 1: Accrue interest and pay minimums
            for d in current_debts:
                if d['balance'] > Decimal('0'):
                    monthly_interest = d['balance'] * (d['rate'] / Decimal('100.0')) / Decimal('12.0')
                    d['balance'] += monthly_interest
                    total_interest_paid += monthly_interest
                    
                    if d['balance'] <= d['min_payment']:
                        available_extra += (d['min_payment'] - d['balance'])
                        d['balance'] = Decimal('0')
                    else:
                        d['balance'] -= d['min_payment']
                        
            # Step 2: Apply extra payments
            if available_extra > Decimal('0') and strategy_type != 'none':
                for d in current_debts:
                    if d['balance'] > Decimal('0'):
                        if d['balance'] <= available_extra:
                            available_extra -= d['balance']
                            d['balance'] = Decimal('0')
                        else:
                            d['balance'] -= available_extra
                            available_extra = Decimal('0')
                            break
            
            total_remaining = sum(d['balance'] for d in current_debts)
            timeline.append({
                'month': months,
                'total_remaining': float(total_remaining)
            })
            
        return {
            'months': months,
            'interest': total_interest_paid,
            'timeline': timeline
        }
        
    def get_plan(self):
        if not self.original_debts:
            return None
            
        # 1. Baseline (Minimum payments only)
        baseline = self._run_simulation('none', Decimal('0'))
        
        # 2. Optimized (With strategy and extra payments)
        optimized = self._run_simulation(self.strategy_type, self.extra_payment)
        
        interest_saved = baseline['interest'] - optimized['interest']
        months_saved = baseline['months'] - optimized['months']
        
        return {
            'baseline': baseline,
            'optimized': optimized,
            'interest_saved': interest_saved if interest_saved > 0 else Decimal('0'),
            'months_saved': months_saved if months_saved > 0 else 0
        }

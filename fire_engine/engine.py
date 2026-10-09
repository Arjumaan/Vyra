from decimal import Decimal
from .models import FIREProfile, FIRESimulationCache

class FIRECalculator:
    def __init__(self, profile: FIREProfile):
        self.profile = profile

    def calculate_fire_number(self, annual_expenses: Decimal) -> Decimal:
        """ Calculates the absolute FIRE number needed """
        swr_decimal = self.profile.safe_withdrawal_rate / Decimal('100.0')
        if swr_decimal <= Decimal('0.00'):
            return Decimal('0.00')
        return annual_expenses / swr_decimal
        
    def calculate_years_to_fire(self, current_net_worth: Decimal, annual_savings: Decimal, annual_expenses: Decimal) -> Decimal:
        """ Basic deterministic projection using a loop for precision over time """
        target = self.calculate_fire_number(annual_expenses)
        if current_net_worth >= target:
            return Decimal('0.0')
            
        real_return = (self.profile.expected_investment_return - self.profile.inflation_rate) / Decimal('100.0')
        
        # If returns are negative and savings are negative, we will never reach it
        if real_return <= Decimal('0.0') and annual_savings <= Decimal('0.0'):
            return Decimal('99.9')
            
        current_wealth = current_net_worth
        years = 0
        timeline = []
        
        # Accumulation Phase (stops exactly at FIRE target)
        while current_wealth < target and years < 60:
            current_wealth = current_wealth * (Decimal('1.0') + real_return) + annual_savings
            years += 1
            timeline.append({
                'year': years,
                'age': self.profile.current_age + years,
                'wealth': float(current_wealth),
                'phase': 'Accumulation'
            })
            
        self.timeline = timeline
        return Decimal(str(years))

    def run_simulation(self) -> FIRESimulationCache:
        """ Runs the full simulation and updates the cache """
        # Import the central wealth calculator
        from wealth.views import _get_wealth_data
        
        # Calculate real-time data if manual overrides aren't provided
        user_wealth_data = _get_wealth_data(self.profile.user)
        
        real_net_worth = Decimal(str(user_wealth_data.get('net_worth', 0)))
        # Assuming this month is representative, annualize it
        real_annual_income = Decimal(str(user_wealth_data.get('this_month_income', 0))) * Decimal('12')
        real_annual_expenses = Decimal(str(user_wealth_data.get('this_month_expenses', 0))) * Decimal('12')
        
        # Fallback defaults if user has absolutely 0 data in the system
        if real_annual_income <= Decimal('0'): real_annual_income = Decimal('1200000.00')
        if real_annual_expenses <= Decimal('0'): real_annual_expenses = Decimal('600000.00')
        if real_net_worth <= Decimal('0'): real_net_worth = Decimal('100000.00')

        annual_expenses = self.profile.manual_annual_expenses or real_annual_expenses
        annual_income = self.profile.manual_annual_income or real_annual_income
        current_net_worth = self.profile.manual_current_net_worth or real_net_worth
        
        annual_savings = annual_income - annual_expenses
        savings_rate = (annual_savings / annual_income * Decimal('100.0')) if annual_income > 0 else Decimal('0.00')
        
        fire_number = self.calculate_fire_number(annual_expenses)
        years_to_fire = self.calculate_years_to_fire(current_net_worth, annual_savings, annual_expenses)
        
        # Update Cache
        cache, _ = FIRESimulationCache.objects.get_or_create(user=self.profile.user)
        cache.calculated_fire_number = round(fire_number, 2)
        cache.years_to_fire = round(years_to_fire, 1)
        cache.current_savings_rate = round(savings_rate, 2)
        
        import json
        if hasattr(self, 'timeline'):
            cache.timeline_data = json.dumps(self.timeline)
            
        cache.save()
        return cache

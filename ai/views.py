from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AIFinancialCoachSession, AIMessage
from wealth.views import _get_wealth_data

from debt_manager.models import Debt
from real_estate.models import Property
from business_ledger.models import BusinessProfile
from fire_engine.models import FIREProfile
from legacy_planner.models import DeadMansSwitch

@login_required
def chat_view(request):
    user = request.user
    
    # Get or create active session
    session = AIFinancialCoachSession.objects.filter(user=user, is_active=True).first()
    if not session:
        session = AIFinancialCoachSession.objects.create(user=user)
        # Generate initial system greeting based on wealth data
        wealth_data = _get_wealth_data(user)
        greeting = f"Hello {user.username}! I'm Vyra AI, your personal Wealth Intelligence Copilot. "
        
        if wealth_data['health_score'] >= 80:
            greeting += f"Your financial health score is excellent ({wealth_data['health_score']}/100). How can we optimize your investments today?"
        elif wealth_data['health_score'] >= 60:
            greeting += f"Your financial health is stable ({wealth_data['health_score']}/100), but there's room to grow. What are your current goals?"
        else:
            greeting += f"Your financial health needs attention ({wealth_data['health_score']}/100). Let's review your cash flow and debt immediately."
            
        AIMessage.objects.create(session=session, sender='ai', content=greeting)

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Save user message
            AIMessage.objects.create(session=session, sender='user', content=user_message)
            
            # AI Logic Context-Aware Engine
            ai_response = _generate_wealth_ai_response(user_message, user)
            AIMessage.objects.create(session=session, sender='ai', content=ai_response)
            
        return redirect('ai_chat')
        
    messages = session.messages.all()
    return render(request, 'ai/chat.html', {'chat_messages': messages})

def _generate_wealth_ai_response(message, user):
    msg = message.lower()
    
    if 'fire' in msg or 'retire' in msg or 'independence' in msg:
        fire_profile = FIREProfile.objects.filter(user=user).first()
        if fire_profile:
            return f"Your FIRE Engine indicates a target age of {fire_profile.target_retirement_age}. With your current safe withdrawal rate of {fire_profile.safe_withdrawal_rate}%, consistency is key. Would you like me to run a Monte Carlo simulation?"
        return "You haven't set up your FIRE profile yet. Head over to the FIRE Engine to calculate when you can achieve financial independence."
        
    elif 'debt' in msg or 'loan' in msg:
        debts = Debt.objects.filter(user=user)
        if debts.exists():
            total = sum(d.principal_balance for d in debts)
            return f"I see you have ₹{total:,.2f} in active debt. Using the Debt Avalanche method (focusing on highest interest first) could save you money. Shall we review your Debt Planner?"
        return "Great news! You currently have no active debts recorded in your Debt Planner."
        
    elif 'business' in msg or 'hustle' in msg:
        businesses = BusinessProfile.objects.filter(user=user)
        if businesses.exists():
            profit = sum(b.net_profit for b in businesses)
            return f"Your business ledger shows a combined net profit of ₹{profit:,.2f}. Remember to mark your business expenses as tax-deductible where applicable!"
        return "I can help you track side-hustles. Check out the Business Ledger to separate your personal and business finances."
        
    elif 'estate' in msg or 'legacy' in msg or 'vault' in msg or 'die' in msg:
        dms = DeadMansSwitch.objects.filter(user=user).first()
        if dms and dms.is_enabled:
            return "Your Legacy Planner and Dead Man's Switch are active. Your digital vault is protected and your trusted contacts are designated."
        return "Your Legacy Planner's Dead Man's Switch is currently inactive. I strongly recommend setting this up to ensure your digital legacy is transferred securely."
        
    elif 'property' in msg or 'real estate' in msg:
        properties = Property.objects.filter(user=user)
        if properties.exists():
            equity = sum(p.equity for p in properties)
            return f"You've built ₹{equity:,.2f} in real estate equity across {properties.count()} properties. Keep an eye on your net yield in the Real Estate portfolio."
        return "You haven't added any properties yet. Use the Real Estate module to track your physical assets and yields."
        
    else:
        return "As your Wealth OS Copilot, I'm analyzing your Cashflow, Debt, Real Estate, Business, and FIRE trajectories. Check the Unified Wealth Hub for a high-level view. How else can I assist you today?"

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AIFinancialCoachSession, AIMessage
from wealth.views import _get_wealth_data

@login_required
def chat_view(request):
    user = request.user
    
    # Get or create active session
    session = AIFinancialCoachSession.objects.filter(user=user, is_active=True).first()
    if not session:
        session = AIFinancialCoachSession.objects.create(user=user)
        # Generate initial system greeting based on wealth data
        wealth_data = _get_wealth_data(user)
        greeting = f"Hello {user.username}! I'm Vyra AI, your personal financial coach. "
        
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
            
            # Simple AI Logic Mock
            ai_response = _generate_mock_ai_response(user_message, user)
            AIMessage.objects.create(session=session, sender='ai', content=ai_response)
            
        return redirect('ai_chat')
        
    messages = session.messages.all()
    return render(request, 'ai/chat.html', {'chat_messages': messages})

def _generate_mock_ai_response(message, user):
    msg = message.lower()
    if 'budget' in msg:
        return "I recommend the 50/30/20 rule. Allocate 50% to needs, 30% to wants, and 20% to savings. Check out your Enterprise Analytics Dashboard for your current breakdown."
    elif 'invest' in msg or 'stock' in msg or 'crypto' in msg:
        return "Before investing heavily, ensure your emergency fund covers at least 3-6 months of your expenses. Have you reviewed your Emergency Fund calculator recently?"
    elif 'debt' in msg or 'loan' in msg or 'emi' in msg:
        return "High-interest debt like credit cards should be prioritized first. Consider the avalanche or snowball method to clear it out."
    else:
        return "That's an interesting point. As your Vyra AI Coach, I suggest reviewing your 'Financial Hub' and 'Insights' regularly. Do you have a specific goal like saving for a house or retirement?"

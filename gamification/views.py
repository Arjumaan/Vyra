from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import VyraScore, UserBadge

@login_required
def gamification_view(request):
    score, created = VyraScore.objects.get_or_create(user=request.user)
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    
    return render(request, 'gamification/dashboard.html', {
        'score': score,
        'user_badges': user_badges,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserSettings, Notification
from .forms import UserSettingsForm

@login_required
def settings_view(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('settings_view')
    else:
        form = UserSettingsForm(instance=user_settings)
        
    return render(request, 'platform_settings/settings.html', {
        'form': form
    })

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST':
        if 'mark_all_read' in request.POST:
            notifications.update(is_read=True)
            messages.success(request, "All notifications marked as read.")
        return redirect('notifications_view')
        
    return render(request, 'platform_settings/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })

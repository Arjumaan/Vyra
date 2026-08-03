from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DatabaseBackup, SecurityLog
from django.utils import timezone

@login_required
def security_center(request):
    # Only superusers can access this view since it is a system-wide platform capability
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('financial_hub')
        
    backups = DatabaseBackup.objects.all()[:10]
    logs = SecurityLog.objects.all()[:20]
    
    return render(request, 'backup/security_center.html', {
        'backups': backups,
        'logs': logs,
    })

@login_required
def trigger_backup(request):
    if not request.user.is_superuser:
        return redirect('financial_hub')
        
    if request.method == 'POST':
        # Simulate backup trigger
        DatabaseBackup.objects.create(status='success', notes='Manual backup triggered by admin')
        SecurityLog.objects.create(user=request.user, action='backup_created', details='Manual backup triggered')
        messages.success(request, "Database backup initiated successfully.")
        
    return redirect('security_center')

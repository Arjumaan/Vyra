from django.contrib import admin
from .models import FIREProfile, FIRESimulationCache

@admin.register(FIREProfile)
class FIREProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_age', 'target_retirement_age', 'safe_withdrawal_rate', 'selected_scenario', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('selected_scenario',)

@admin.register(FIRESimulationCache)
class FIRESimulationCacheAdmin(admin.ModelAdmin):
    list_display = ('user', 'calculated_fire_number', 'years_to_fire', 'projected_fire_date', 'current_savings_rate', 'last_calculated')
    search_fields = ('user__username', 'user__email')

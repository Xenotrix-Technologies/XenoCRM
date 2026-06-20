from django.contrib import admin
from .models import Organization, UserProfile, Lead, Activity, Task, Meeting

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'role')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'score', 'status', 'stage', 'value', 'organization', 'owner')
    list_filter = ('status', 'stage', 'organization')
    search_fields = ('name', 'company', 'email')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'type', 'timestamp', 'description')
    list_filter = ('type', 'timestamp')
    search_fields = ('lead__name', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'lead', 'due_date', 'priority', 'completed')
    list_filter = ('priority', 'completed', 'due_date')
    search_fields = ('description', 'lead__name')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'lead', 'date_time', 'location')
    list_filter = ('date_time', 'location')
    search_fields = ('title', 'lead__name')

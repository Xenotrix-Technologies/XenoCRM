from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('organization', 'name')
        db_table = 'departments'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=100, default='Sales Executive')
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    custom_permissions_json = models.TextField(default='{}')

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

    SETTINGS_SUBPAGES = [
        'content_settings',
        'lead_statuses',
        'services',
        'staff_roles',
        'notification_settings',
        'role_permissions',
        'departments',
    ]

    def check_page_permission(self, page_name):
        from crm.models import StaffRole
        import json
        
        role_lower = self.role.lower()
        view_key = f"{role_lower}_{page_name}"
        settings_key = f"{role_lower}_settings"
        
        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if view_key in custom_perms:
                val = custom_perms[view_key]
                return val is True or val == True or val == "true"
            if page_name in self.SETTINGS_SUBPAGES and settings_key in custom_perms:
                val = custom_perms[settings_key]
                if val is True or val == True or val == "true":
                    return True
                return False  # If explicitly false in overrides, deny
        except Exception:
            pass

        # 2. Check Role-level permissions
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            settings_val = perms.get(settings_key)
            if page_name in self.SETTINGS_SUBPAGES and (settings_val is True or settings_val == True or settings_val == "true"):
                return True
            val = perms.get(view_key)
            if val is not None:
                return val is True or val == True or val == "true"
            if page_name in self.SETTINGS_SUBPAGES and settings_val is not None:
                return False
        except Exception:
            pass
            
        # 3. Defaults fallback logic
        if 'admin' in role_lower:
            return True
        elif 'manager' in role_lower:
            return page_name not in ['settings', 'staff'] and page_name not in self.SETTINGS_SUBPAGES and page_name != 'content_tracker'
        else:
            return page_name in ['dashboard', 'leads', 'calendar', 'clients', 'support']

    @property
    def has_access_dashboard(self):
        return self.check_page_permission('dashboard')

    @property
    def has_access_leads(self):
        return self.check_page_permission('leads')

    @property
    def has_access_calendar(self):
        return self.check_page_permission('calendar')

    @property
    def has_access_clients(self):
        return self.check_page_permission('clients')

    @property
    def has_access_support(self):
        return self.check_page_permission('support')

    @property
    def has_access_projects(self):
        return self.check_page_permission('projects')

    @property
    def has_access_agreements(self):
        return self.check_page_permission('agreements')

    @property
    def has_access_campaigns(self):
        return self.check_page_permission('campaigns')

    @property
    def has_access_staff(self):
        return self.check_page_permission('staff')

    @property
    def has_access_content_tracker(self):
        return self.check_page_permission('content_tracker')

    @property
    def has_access_settings(self):
        return self.check_page_permission('settings')

    @property
    def has_access_content_settings(self):
        return self.check_page_permission('content_settings')

    @property
    def has_access_lead_statuses(self):
        return self.check_page_permission('lead_statuses')

    @property
    def has_access_services(self):
        return self.check_page_permission('services')

    @property
    def has_access_staff_roles(self):
        return self.check_page_permission('staff_roles')

    @property
    def has_access_notification_settings(self):
        return self.check_page_permission('notification_settings')

    @property
    def has_access_role_permissions(self):
        return self.check_page_permission('role_permissions')

    @property
    def has_access_departments(self):
        return self.check_page_permission('departments')

    def check_edit_permission(self, page_name):
        """Check whether the user's role has edit access for a given page."""
        from crm.models import StaffRole
        import json
        role_lower = self.role.lower()
        edit_key = f"{role_lower}_{page_name}_edit"

        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if edit_key in custom_perms:
                val = custom_perms[edit_key]
                return val is True or val == True or val == "true"
        except Exception:
            pass

        # 2. Check Role-level permissions
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            val = perms.get(edit_key)
            if val is not None:
                return val is True or val == True or val == "true"
        except Exception:
            pass
            
        # 3. Default: admins get edit, others don't
        if 'admin' in role_lower:
            return True
        return False

    @property
    def has_edit_dashboard(self):
        return self.check_edit_permission('dashboard')

    @property
    def has_edit_leads(self):
        return self.check_edit_permission('leads')

    @property
    def has_edit_calendar(self):
        return self.check_edit_permission('calendar')

    @property
    def has_edit_clients(self):
        return self.check_edit_permission('clients')

    @property
    def has_edit_support(self):
        return self.check_edit_permission('support')

    @property
    def has_edit_projects(self):
        return self.check_edit_permission('projects')

    @property
    def has_edit_agreements(self):
        return self.check_edit_permission('agreements')

    @property
    def has_edit_campaigns(self):
        return self.check_edit_permission('campaigns')

    @property
    def has_edit_staff(self):
        return self.check_edit_permission('staff')

    @property
    def has_edit_content_tracker(self):
        return self.check_edit_permission('content_tracker')

    @property
    def has_edit_settings(self):
        return self.check_edit_permission('settings')

    @property
    def has_edit_content_settings(self):
        return self.check_edit_permission('content_settings')

    @property
    def has_edit_lead_statuses(self):
        return self.check_edit_permission('lead_statuses')

    @property
    def has_edit_services(self):
        return self.check_edit_permission('services')

    @property
    def has_edit_staff_roles(self):
        return self.check_edit_permission('staff_roles')

    @property
    def has_edit_notification_settings(self):
        return self.check_edit_permission('notification_settings')

    @property
    def has_edit_role_permissions(self):
        return self.check_edit_permission('role_permissions')

    @property
    def has_edit_departments(self):
        return self.check_edit_permission('departments')

    def check_delete_permission(self, page_name):
        """Check whether the user's role has delete access for a given page."""
        from crm.models import StaffRole
        import json
        role_lower = self.role.lower()
        delete_key = f"{role_lower}_{page_name}_delete"

        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if delete_key in custom_perms:
                val = custom_perms[delete_key]
                return val is True or val == True or val == "true"
        except Exception:
            pass

        # 2. Check Role-level permissions
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            val = perms.get(delete_key)
            if val is not None:
                return val is True or val == True or val == "true"
        except Exception:
            pass
            
        # 3. Default: only admins get delete
        if 'admin' in role_lower:
            return True
        return False

    @property
    def has_delete_dashboard(self):
        return self.check_delete_permission('dashboard')

    @property
    def has_delete_leads(self):
        return self.check_delete_permission('leads')

    @property
    def has_delete_calendar(self):
        return self.check_delete_permission('calendar')

    @property
    def has_delete_clients(self):
        return self.check_delete_permission('clients')

    @property
    def has_delete_support(self):
        return self.check_delete_permission('support')

    @property
    def has_delete_projects(self):
        return self.check_delete_permission('projects')

    @property
    def has_delete_agreements(self):
        return self.check_delete_permission('agreements')

    @property
    def has_delete_campaigns(self):
        return self.check_delete_permission('campaigns')

    @property
    def has_delete_staff(self):
        return self.check_delete_permission('staff')

    @property
    def has_delete_content_tracker(self):
        return self.check_delete_permission('content_tracker')

    @property
    def has_delete_settings(self):
        return self.check_delete_permission('settings')

    @property
    def has_delete_content_settings(self):
        return self.check_delete_permission('content_settings')

    @property
    def has_delete_lead_statuses(self):
        return self.check_delete_permission('lead_statuses')

    @property
    def has_delete_services(self):
        return self.check_delete_permission('services')

    @property
    def has_delete_staff_roles(self):
        return self.check_delete_permission('staff_roles')

    @property
    def has_delete_notification_settings(self):
        return self.check_delete_permission('notification_settings')

    @property
    def has_delete_role_permissions(self):
        return self.check_delete_permission('role_permissions')

    @property
    def has_delete_departments(self):
        return self.check_delete_permission('departments')

    @property
    def has_any_settings_access(self):
        return (
            self.has_access_settings or
            self.has_access_content_settings or
            self.has_access_lead_statuses or
            self.has_access_services or
            self.has_access_staff_roles or
            self.has_access_notification_settings or
            self.has_access_role_permissions or
            self.has_access_departments
        )

class StaffRole(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff_roles')
    name = models.CharField(max_length=100)

    permissions_json = models.TextField(default='{}')

    class Meta:
        unique_together = ('organization', 'name')
        db_table = 'staff_roles'

    def __str__(self):
        return self.name

class SystemNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='system_notifications')
    message = models.TextField()
    type = models.CharField(max_length=50, default='info') # success, error, info
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.user.username}"

class StatusStyleMixin:
    @property
    def color_hex(self):
        if getattr(self, 'color', '').startswith('#'):
            return self.color
        color_map = {
            'blue': '#0053db', 'grey': '#64748b', 'green': '#10b981', 
            'yellow': '#f59e0b', 'red': '#ef4444', 'orange': '#f97316', 
            'purple': '#a855f7', 'pink': '#ec4899', 'teal': '#14b8a6',
        }
        return color_map.get(getattr(self, 'color', '').lower(), '#64748b')

    @property
    def badge_style(self):
        hex_val = self.color_hex
        return f"background-color: {hex_val}1a; color: {hex_val}; border: 1px solid {hex_val}33;"

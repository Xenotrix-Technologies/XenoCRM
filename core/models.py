from django.db import models
from django.contrib.auth.models import User
import json


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


class StaffRole(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff_roles')
    name = models.CharField(max_length=100)
    permissions_json = models.TextField(default='{}')

    class Meta:
        unique_together = ('organization', 'name')
        db_table = 'staff_roles'

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
        'leads_settings',
        'calendar_status',
        'calendar_status_settings',
        'clients_status',
        'client_status_settings',
        'support_status',
        'ticket_status_settings',
        'projects_status',
        'project_status_settings',
        'campaigns_status',
        'campaign_status_settings',
        'finance_status',
        'finance_status_settings',
        'services',
        'staff_roles',
        'notification_settings',
        'role_permissions',
        'departments',
    ]

    PERMISSION_ALIASES = {
        'lead_statuses': 'leads_settings',
        'leads_settings': 'lead_statuses',
        'calendar_status': 'calendar_status_settings',
        'calendar_status_settings': 'calendar_status',
        'clients_status': 'client_status_settings',
        'client_status_settings': 'clients_status',
        'support_status': 'ticket_status_settings',
        'ticket_status_settings': 'support_status',
        'projects_status': 'project_status_settings',
        'project_status_settings': 'projects_status',
        'campaigns_status': 'campaign_status_settings',
        'campaign_status_settings': 'campaigns_status',
        'cms_settings': 'content_settings',
        'content_settings': 'cms_settings',
        'finance_status': 'finance_status_settings',
        'finance_status_settings': 'finance_status',
        'staff': 'hr_employees',
        'hr_employees': 'staff',
        'campaigns': 'campaign',
        'campaign': 'campaigns',
    }

    def check_page_permission(self, page_name):
        if self.user and self.user.is_superuser:
            return True

        role_lower = (self.role or '').lower().strip()
        if 'admin' in role_lower:
            return True

        pages_to_check = [page_name]
        alias = self.PERMISSION_ALIASES.get(page_name)
        if alias and alias not in pages_to_check:
            pages_to_check.append(alias)

        candidate_prefixes = set([
            role_lower,
            role_lower.replace(' ', '_'),
            role_lower.replace('-', '_'),
            'employee',
            'administrator',
            'admin',
            'sales executive',
            'sales_executive',
            'manager',
        ])

        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if custom_perms:
                for p in pages_to_check:
                    for prefix in candidate_prefixes:
                        vk = f"{prefix}_{p}"
                        if vk in custom_perms:
                            val = custom_perms[vk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True
                    if p in custom_perms:
                        val = custom_perms[p]
                        if val is True or val == True or str(val).lower() == 'true':
                            return True
                    for k, val in custom_perms.items():
                        if k.endswith(f"_{p}") and (val is True or val == True or str(val).lower() == 'true'):
                            return True

                    for prefix in candidate_prefixes:
                        sk = f"{prefix}_settings"
                        if (p in self.SETTINGS_SUBPAGES or 'status' in p or 'settings' in p) and sk in custom_perms:
                            val = custom_perms[sk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True

                    main_module = p.split('_')[0] if '_' in p else p
                    for prefix in candidate_prefixes:
                        mk = f"{prefix}_{main_module}"
                        if mk in custom_perms:
                            val = custom_perms[mk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True
        except Exception:
            pass

        # 2. Check Role-level permissions
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json or '{}')
            if perms:
                for p in pages_to_check:
                    for prefix in candidate_prefixes:
                        vk = f"{prefix}_{p}"
                        if vk in perms:
                            val = perms[vk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True
                    if p in perms:
                        val = perms[p]
                        if val is True or val == True or str(val).lower() == 'true':
                            return True
                    for k, val in perms.items():
                        if k.endswith(f"_{p}") and (val is True or val == True or str(val).lower() == 'true'):
                            return True

                    for prefix in candidate_prefixes:
                        sk = f"{prefix}_settings"
                        if (p in self.SETTINGS_SUBPAGES or 'status' in p or 'settings' in p) and sk in perms:
                            val = perms[sk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True

                    main_module = p.split('_')[0] if '_' in p else p
                    for prefix in candidate_prefixes:
                        mk = f"{prefix}_{main_module}"
                        if mk in perms:
                            val = perms[mk]
                            if val is True or val == True or str(val).lower() == 'true':
                                return True
        except Exception:
            pass

        # 3. Defaults fallback logic
        if 'admin' in role_lower:
            return True
        elif 'manager' in role_lower:
            return page_name not in ['role_permissions', 'notification_settings']
        else:
            return page_name in [
                'dashboard', 'leads', 'calendar', 'clients', 'support', 'projects',
                'hr', 'finance', 'agreements', 'campaigns', 'cms', 'staff', 'services',
                'lead_statuses', 'leads_settings', 'clients_status', 'projects_status',
                'campaigns_status', 'calendar_status', 'support_status', 'finance_status'
            ]

    @property
    def has_access_dashboard(self):
        return self.check_page_permission('dashboard')

    @property
    def has_access_leads(self):
        return self.check_page_permission('leads')

    @property
    def has_access_leads_settings(self):
        return self.check_page_permission('leads_settings') or self.check_page_permission('lead_statuses')

    @property
    def has_access_lead_statuses(self):
        return self.check_page_permission('lead_statuses') or self.check_page_permission('leads_settings')

    @property
    def has_access_calendar(self):
        return self.check_page_permission('calendar')

    @property
    def has_access_calendar_status(self):
        return self.check_page_permission('calendar_status')

    @property
    def has_access_calendar_status_settings(self):
        return self.check_page_permission('calendar_status')

    @property
    def has_access_clients(self):
        return self.check_page_permission('clients')

    @property
    def has_access_clients_status(self):
        return self.check_page_permission('clients_status')

    @property
    def has_access_client_status_settings(self):
        return self.check_page_permission('clients_status')

    @property
    def has_access_support(self):
        return self.check_page_permission('support')

    @property
    def has_access_support_status(self):
        return self.check_page_permission('support_status')

    @property
    def has_access_ticket_status_settings(self):
        return self.check_page_permission('support_status')

    @property
    def has_access_projects(self):
        return self.check_page_permission('projects')

    @property
    def has_access_projects_status(self):
        return self.check_page_permission('projects_status')

    @property
    def has_access_project_status_settings(self):
        return self.check_page_permission('projects_status')

    @property
    def has_access_hr(self):
        return self.check_page_permission('hr')

    @property
    def has_access_hr_dashboard(self):
        return self.check_page_permission('hr') or self.check_page_permission('staff')

    @property
    def has_access_staff(self):
        return self.check_page_permission('staff')

    @property
    def has_access_hr_attendance(self):
        return self.check_page_permission('hr')

    @property
    def has_access_hr_leaves(self):
        return self.check_page_permission('hr')

    @property
    def has_access_hr_payroll(self):
        return self.check_page_permission('hr')

    @property
    def has_access_hr_settings(self):
        return self.check_page_permission('hr')

    @property
    def has_access_finance(self):
        return self.check_page_permission('finance')

    @property
    def has_access_finance_dashboard(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_dashboard')

    @property
    def has_access_finance_invoices(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_invoices')

    @property
    def has_access_finance_income(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_income')

    @property
    def has_access_finance_expenses(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_expenses')

    @property
    def has_access_finance_reports(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_reports')

    @property
    def has_access_partner_payouts(self):
        return self.check_page_permission('finance') or self.check_page_permission('partner_payouts')

    @property
    def has_access_finance_settings(self):
        return self.check_page_permission('finance') or self.check_page_permission('finance_settings')

    @property
    def has_access_finance_status(self):
        return self.check_page_permission('finance_status')

    @property
    def has_access_finance_status_settings(self):
        return self.check_page_permission('finance_status')

    @property
    def has_access_agreements(self):
        return self.check_page_permission('agreements')

    @property
    def has_access_campaigns(self):
        return self.check_page_permission('campaigns')

    @property
    def has_access_campaigns_status(self):
        return self.check_page_permission('campaigns_status')

    @property
    def has_access_campaign_status_settings(self):
        return self.check_page_permission('campaigns_status')

    @property
    def has_access_cms(self):
        return self.check_page_permission('cms')

    @property
    def has_access_cms_settings(self):
        return self.check_page_permission('content_settings')

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

    @property
    def has_any_settings_access(self):
        return (
            self.has_access_cms_settings or
            self.has_access_leads_settings or
            self.has_access_lead_statuses or
            self.has_access_clients_status or
            self.has_access_projects_status or
            self.has_access_campaigns_status or
            self.has_access_calendar_status or
            self.has_access_support_status or
            self.has_access_finance_status or
            self.has_access_services or
            self.has_access_staff_roles or
            self.has_access_notification_settings or
            self.has_access_role_permissions or
            self.has_access_departments or
            self.has_access_finance_settings
        )

    def check_edit_permission(self, page_name):
        role_lower = self.role.lower()
        if 'admin' in role_lower:
            return True
        edit_key = f"{page_name}-edit"
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if edit_key in custom_perms:
                val = custom_perms[edit_key]
                return val is True or val == True or val == "true"
        except Exception:
            pass
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            val = perms.get(edit_key)
            if val is not None:
                return val is True or val == True or val == "true"
        except Exception:
            pass
        return self.check_page_permission(page_name)

    def check_delete_permission(self, page_name):
        role_lower = self.role.lower()
        if 'admin' in role_lower:
            return True
        delete_key = f"{page_name}-delete"
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            if delete_key in custom_perms:
                val = custom_perms[delete_key]
                return val is True or val == True or val == "true"
        except Exception:
            pass
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            val = perms.get(delete_key)
            if val is not None:
                return val is True or val == True or val == "true"
        except Exception:
            pass
        return self.check_page_permission(page_name)


class SystemNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='system_notifications')
    message = models.TextField()
    type = models.CharField(max_length=50, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.user.username}"

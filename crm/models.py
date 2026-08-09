from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
        'leads_settings',
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
        from crm.models import StaffRole
        import json
        
        role_lower = self.role.lower()
        pages_to_check = [page_name]
        alias = self.PERMISSION_ALIASES.get(page_name)
        if alias and alias not in pages_to_check:
            pages_to_check.append(alias)
        
        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            for p in pages_to_check:
                view_key = f"{role_lower}_{p}"
                if view_key in custom_perms:
                    val = custom_perms[view_key]
                    return val is True or val == True or val == "true"
                settings_key = f"{role_lower}_settings"
                if p in self.SETTINGS_SUBPAGES and settings_key in custom_perms:
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
            for p in pages_to_check:
                settings_key = f"{role_lower}_settings"
                settings_val = perms.get(settings_key)
                if p in self.SETTINGS_SUBPAGES and (settings_val is True or settings_val == True or settings_val == "true"):
                    return True
                view_key = f"{role_lower}_{p}"
                val = perms.get(view_key)
                if val is not None:
                    return val is True or val == True or val == "true"
                if p in self.SETTINGS_SUBPAGES and settings_val is not None:
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
    def has_access_leads_settings(self):
        return self.check_page_permission('leads_settings')

    @property
    def has_access_calendar(self):
        return self.check_page_permission('calendar')

    @property
    def has_access_calendar_status(self):
        return self.check_page_permission('calendar_status')

    @property
    def has_access_clients(self):
        return self.check_page_permission('clients')

    @property
    def has_access_clients_status(self):
        return self.check_page_permission('clients_status')

    @property
    def has_access_support(self):
        return self.check_page_permission('support')

    @property
    def has_access_support_status(self):
        return self.check_page_permission('support_status')

    @property
    def has_access_projects(self):
        return self.check_page_permission('projects')

    @property
    def has_access_projects_status(self):
        return self.check_page_permission('projects_status')

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
    def has_access_hr(self):
        return self.check_page_permission('hr')

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
    def has_access_cms_settings(self):
        return self.check_page_permission('cms_settings')

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

    @property
    def has_access_finance(self):
        return self.check_page_permission('finance')

    @property
    def has_access_finance_status(self):
        return self.check_page_permission('finance_status')

    @property
    def has_access_partner_payouts(self):
        return self.check_page_permission('partner_payouts')

    @property
    def has_access_cms(self):
        return (self.check_page_permission('content_tracker') or 
                self.check_page_permission('cms_settings') or 
                self.check_page_permission('content_settings') or 
                self.check_page_permission('editor_dashboard') or 
                self.check_page_permission('editor_board'))

    @property
    def has_access_hr_dashboard(self):
        return self.check_page_permission('hr_dashboard')

    @property
    def has_access_hr_employees(self):
        return self.check_page_permission('hr_employees')

    @property
    def has_access_hr_attendance(self):
        return self.check_page_permission('hr_attendance')

    @property
    def has_access_hr_leaves(self):
        return self.check_page_permission('hr_leaves')

    @property
    def has_access_hr_payroll(self):
        return self.check_page_permission('hr_payroll')

    @property
    def has_access_hr_settings(self):
        return self.check_page_permission('hr_settings')

    @property
    def has_access_finance_dashboard(self):
        return self.check_page_permission('finance_dashboard')

    @property
    def has_access_finance_income(self):
        return self.check_page_permission('finance_income')

    @property
    def has_access_finance_expenses(self):
        return self.check_page_permission('finance_expenses')

    @property
    def has_access_finance_reports(self):
        return self.check_page_permission('finance_reports')

    @property
    def has_access_finance_settings(self):
        return self.check_page_permission('finance_settings')

    @property
    def has_access_finance_invoices(self):
        return self.check_page_permission('finance_invoices')

    @property
    def has_access_editor_dashboard(self):
        return self.check_page_permission('editor_dashboard')

    @property
    def has_access_editor_board(self):
        return self.check_page_permission('editor_board')

    @property
    def has_access_post_management(self):
        return self.check_page_permission('post_management')

    @property
    def has_access_campaign_status_settings(self):
        return self.check_page_permission('campaign_status_settings')



    def check_edit_permission(self, page_name):
        """Check whether the user's role has edit access for a given page."""
        from crm.models import StaffRole
        import json
        role_lower = self.role.lower()
        pages_to_check = [page_name]
        alias = self.PERMISSION_ALIASES.get(page_name)
        if alias and alias not in pages_to_check:
            pages_to_check.append(alias)

        # 1. Check Staff-specific overrides first
        try:
            custom_perms = json.loads(self.custom_permissions_json or '{}')
            for p in pages_to_check:
                edit_key = f"{role_lower}_{p}_edit"
                if edit_key in custom_perms:
                    val = custom_perms[edit_key]
                    return val is True or val == True or val == "true"
        except Exception:
            pass

        # 2. Check Role-level permissions
        try:
            role_obj = StaffRole.objects.get(organization=self.organization, name=self.role)
            perms = json.loads(role_obj.permissions_json)
            for p in pages_to_check:
                edit_key = f"{role_lower}_{p}_edit"
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


    @property

    def has_edit_finance(self):

        return self.check_edit_permission('finance')

    @property

    def has_edit_partner_payouts(self):

        return self.check_edit_permission('partner_payouts')

    @property

    def has_edit_cms(self):

        return self.check_edit_permission('cms')

    @property

    def has_edit_hr_dashboard(self):

        return self.check_edit_permission('hr_dashboard')

    @property

    def has_edit_hr_employees(self):

        return self.check_edit_permission('hr_employees')

    @property

    def has_edit_hr_attendance(self):

        return self.check_edit_permission('hr_attendance')

    @property

    def has_edit_hr_leaves(self):

        return self.check_edit_permission('hr_leaves')

    @property

    def has_edit_hr_payroll(self):

        return self.check_edit_permission('hr_payroll')

    @property

    def has_edit_hr_settings(self):

        return self.check_edit_permission('hr_settings')

    @property

    def has_edit_finance_dashboard(self):

        return self.check_edit_permission('finance_dashboard')

    @property

    def has_edit_finance_income(self):

        return self.check_edit_permission('finance_income')

    @property

    def has_edit_finance_expenses(self):

        return self.check_edit_permission('finance_expenses')

    @property

    def has_edit_finance_reports(self):

        return self.check_edit_permission('finance_reports')

    @property

    def has_edit_finance_settings(self):

        return self.check_edit_permission('finance_settings')

    @property

    def has_edit_editor_dashboard(self):

        return self.check_edit_permission('editor_dashboard')

    @property

    def has_edit_editor_board(self):

        return self.check_edit_permission('editor_board')

    @property

    def has_edit_post_management(self):

        return self.check_edit_permission('post_management')

    @property

    def has_edit_campaign_status_settings(self):

        return self.check_edit_permission('campaign_status_settings')



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

    def has_delete_finance(self):

        return self.check_delete_permission('finance')

    @property

    def has_delete_partner_payouts(self):

        return self.check_delete_permission('partner_payouts')

    @property

    def has_delete_cms(self):

        return self.check_delete_permission('cms')

    @property

    def has_delete_hr_dashboard(self):

        return self.check_delete_permission('hr_dashboard')

    @property

    def has_delete_hr_employees(self):

        return self.check_delete_permission('hr_employees')

    @property

    def has_delete_hr_attendance(self):

        return self.check_delete_permission('hr_attendance')

    @property

    def has_delete_hr_leaves(self):

        return self.check_delete_permission('hr_leaves')

    @property

    def has_delete_hr_payroll(self):

        return self.check_delete_permission('hr_payroll')

    @property

    def has_delete_hr_settings(self):

        return self.check_delete_permission('hr_settings')

    @property

    def has_delete_finance_dashboard(self):

        return self.check_delete_permission('finance_dashboard')

    @property

    def has_delete_finance_income(self):

        return self.check_delete_permission('finance_income')

    @property

    def has_delete_finance_expenses(self):

        return self.check_delete_permission('finance_expenses')

    @property

    def has_delete_finance_reports(self):

        return self.check_delete_permission('finance_reports')

    @property

    def has_delete_finance_settings(self):

        return self.check_delete_permission('finance_settings')

    @property

    def has_delete_editor_dashboard(self):

        return self.check_delete_permission('editor_dashboard')

    @property

    def has_delete_editor_board(self):

        return self.check_delete_permission('editor_board')

    @property

    def has_delete_post_management(self):

        return self.check_delete_permission('post_management')

    @property

    def has_delete_campaign_status_settings(self):

        return self.check_delete_permission('campaign_status_settings')



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


class LeadStatus(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#0053db')
    position = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'lead_statuses'

    def __str__(self):
        return self.name

    @property
    def color_hex(self):
        color_map = {
            'blue': '#0053db',
            'grey': '#64748b',
            'green': '#10b981',
            'yellow': '#f59e0b',
            'red': '#ef4444',
            'orange': '#f97316',
            'purple': '#a855f7',
            'pink': '#ec4899',
            'teal': '#14b8a6',
        }
        if self.color.startswith('#'):
            return self.color
        return color_map.get(self.color.lower(), '#0053db')

    @property
    def badge_style(self):
        hex_val = self.color_hex
        return f"background-color: {hex_val}1a; color: {hex_val}; border: 1px solid {hex_val}33;"

    @property
    def badge_class(self):
        return ''


def get_default_badge_class(status):
    if status == 'Qualified':
        return 'bg-primary-container/10 text-primary border border-primary/20'
    elif status == 'Contacted':
        return 'bg-surface-variant text-on-surface-variant border border-outline-variant/30'
    elif status == 'New':
        return 'bg-tertiary-container/20 text-tertiary border border-tertiary/20'
    elif status == 'Cold Lead':
        return 'bg-error-container/40 text-error border border-error/20'
    return 'bg-error/10 text-error border border-error/20'


class Lead(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Cold Lead', 'Cold Lead'),
        ('Lost', 'Lost'),
    ]

    STAGE_CHOICES = [
        ('New', 'New'),
        ('Qualified', 'Qualified'),
        ('Proposal', 'Proposal'),
        ('Negotiation', 'Negotiation'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    alt_phone_number = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255)
    score = models.IntegerField(default=50) # Lead score 0-100
    status = models.CharField(max_length=50, default='New')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='New')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_leads')
    services = models.ManyToManyField('Service', blank=True, related_name='leads')
    lifecycle_stage = models.CharField(max_length=100, default='Prospect')
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    health_score = models.IntegerField(default=50)
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    last_followup_date_time = models.DateTimeField(blank=True, null=True)
    followup_wanted_date_time = models.DateTimeField(blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_client = models.BooleanField(default=False)

    class Meta:
        db_table = 'leads'

    @property
    def status_badge_style(self):
        try:
            if self.is_client:
                status_obj = ClientStatus.objects.filter(organization=self.organization, name=self.status).first()
            else:
                status_obj = LeadStatus.objects.filter(organization=self.organization, name=self.status).first()
            if status_obj:
                return status_obj.badge_style
        except Exception:
            pass
        # Fallback to default colors
        color_map = {
            'New': '#10b981',
            'Contacted': '#64748b',
            'Qualified': '#0053db',
            'Cold Lead': '#ef4444',
            'Lost': '#ef4444',
            'Active': '#10b981',
            'Completed': '#0053db',
        }
        hex_val = color_map.get(self.status, '#0053db')
        return f"background-color: {hex_val}1a; color: {hex_val}; border: 1px solid {hex_val}33;"

    @property
    def status_badge_class(self):
        if hasattr(self, '_badge_class'):
            return self._badge_class
        try:
            if self.is_client:
                status_obj = ClientStatus.objects.filter(organization=self.organization, name=self.status).first()
            else:
                status_obj = LeadStatus.objects.filter(organization=self.organization, name=self.status).first()
            if status_obj:
                self._badge_class = status_obj.badge_class
                return self._badge_class
        except Exception:
            pass
        return get_default_badge_class(self.status)

    def __str__(self):
        return f"{self.name} - {self.company}"

class Activity(models.Model):
    TYPE_CHOICES = [
        ('Email', 'Email'),
        ('Call', 'Call'),
        ('Meeting', 'Meeting'),
        ('Task', 'Task'),
        ('Stage Update', 'Stage Update'),
        ('Creation', 'Creation'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.type} on {self.lead.name} at {self.timestamp}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=255, default='Project Task')
    description = models.TextField(blank=True, null=True)
    assignees = models.ManyToManyField(UserProfile, blank=True, related_name='assigned_tasks')
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    status = models.ForeignKey('ProjectStatus', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tasks'

    def __str__(self):
        return f"{self.description} ({'Completed' if self.completed else 'Pending'})"

class Meeting(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='meetings')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings')
    title = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255, default='Zoom')

    class Meta:
        db_table = 'meetings'

    def __str__(self):
        return f"{self.title} at {self.date_time}"

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recurring = models.BooleanField(default=False)
    color = models.CharField(max_length=50, default='#004ac6')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')
    notified_10h = models.BooleanField(default=False)
    notified_1h = models.BooleanField(default=False)

    class Meta:
        db_table = 'events'

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"


class StaffRole(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff_roles')
    name = models.CharField(max_length=100)

    permissions_json = models.TextField(default='{}')

    class Meta:
        unique_together = ('organization', 'name')
        db_table = 'staff_roles'

    def __str__(self):
        return self.name


class Service(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'services'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ticket(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tickets')
    ticket_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Open')
    priority = models.CharField(max_length=50, default='Medium')
    assignee = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    project = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"


class Agreement(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='agreements')
    agreement_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    client_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)
    client_phone = models.CharField(max_length=50, blank=True, null=True)
    client_address = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='agreements')
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    advance_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_cycle = models.CharField(max_length=100, default='Monthly')
    payment_method = models.CharField(max_length=100, default='Bank Transfer')
    posts_count = models.IntegerField(default=0)
    campaigns_count = models.IntegerField(default=0)
    revisions = models.IntegerField(default=3)
    notice_period = models.IntegerField(default=30)
    notes = models.TextField(blank=True, null=True)
    project_estimation_json = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agreements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agreement_number} - {self.client_name}"

    @property
    def parsed_estimation(self):
        import json
        if self.project_estimation_json:
            try:
                return json.loads(self.project_estimation_json)
            except Exception:
                pass
        return None


class AgreementService(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'agreement_services'

    def __str__(self):
        return self.title


class ClientResponsibility(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='responsibilities')
    responsibility = models.TextField()

    class Meta:
        db_table = 'client_responsibilities'

    def __str__(self):
        return self.responsibility[:50]


class Deliverable(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='deliverables')
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'deliverables'

    def __str__(self):
        return self.title


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Planning')
    leads_generated = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campaigns'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Editing', 'Editing'),
        ('Review', 'Review'),
        ('Approved', 'Approved'),
        ('Published', 'Published'),
        ('Rejected', 'Rejected'),
        ('Scheduled', 'Scheduled'),
    ]

    CAMPAIGN_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Planning', 'Planning'),
        ('In Progress', 'In Progress'),
        ('Paused', 'Paused'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='content_items')
    client = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='content_items')
    video_title = models.CharField(max_length=255)
    editor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_content')
    date_received = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    platform = models.CharField(max_length=50)
    upload_date = models.DateField(null=True, blank=True)
    post_type = models.CharField(max_length=50)
    campaign_status = models.CharField(max_length=50, choices=CAMPAIGN_STATUS_CHOICES, default='Not Started')
    video_link = models.URLField(max_length=1000, blank=True, null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    notes = models.TextField(blank=True, null=True)
    client_month = models.CharField(max_length=50, blank=True, null=True)
    editor_month = models.CharField(max_length=50, blank=True, null=True)
    campaign_run_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'Published':
            Campaign.objects.get_or_create(
                organization=self.organization,
                name=self.video_title,
                defaults={'status': 'Active'}
            )

    class Meta:
        db_table = 'content_items'
        ordering = ['-due_date', '-created_at']

    def __str__(self):
        return f"{self.video_title} ({self.client.name})"


class ContentDropdownOption(models.Model):
    """Dynamic dropdown options for the Content Tracker (platforms, post types, statuses, etc.)."""
    CATEGORY_CHOICES = [
        ('platform', 'Platform'),
        ('post_type', 'Post Type'),
        ('status', 'Status'),
        ('campaign_status', 'Campaign Status'),
        ('priority', 'Priority'),
        ('editor_status', 'Editor Board Status'),
        ('marketer_status', 'Post Management Status'),
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='content_dropdown_options')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    value = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'content_dropdown_options'
        ordering = ['category', 'display_order', 'value']
        unique_together = ('organization', 'category', 'value')

    def __str__(self):
        return f"{self.get_category_display()}: {self.value}"

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


class FinancePaymentMethod(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_payment_methods')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinanceExpenseCategory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_expense_categories')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinancePaymentStatus(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_payment_statuses')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinanceCommissionType(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_commission_types')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Income(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='incomes')
    date = models.DateField()
    client_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incomes'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.amount}"


class Expense(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.ForeignKey(FinanceExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cost_center = models.CharField(max_length=150, blank=True, null=True)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount}"


class PartnerPayout(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='partner_payouts')
    payout_id = models.CharField(max_length=50)
    partner_name = models.CharField(max_length=255)
    project_client = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(FinancePaymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    commission_type = models.ForeignKey(FinanceCommissionType, on_delete=models.SET_NULL, null=True, blank=True)
    payout_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partner_payouts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payout_id} - {self.partner_name} - {self.status}"


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

class ClientStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='client_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'client_statuses'
    def __str__(self): return self.name

class ProjectStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='project_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'project_statuses'
    def __str__(self): return self.name

class CampaignStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaign_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'campaign_statuses'
    def __str__(self): return self.name

class CalendarStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='calendar_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'calendar_statuses'
    def __str__(self): return self.name

class TicketStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ticket_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'ticket_statuses'
    def __str__(self): return self.name

class PriorityStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='priority_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'priority_statuses'
    def __str__(self): return self.name

class InvoiceStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoice_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'invoice_statuses'
    def __str__(self): return self.name

class Invoice(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices')
    
    # Customer Info
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Invoice Info
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')
    currency = models.CharField(max_length=10, default='INR')
    
    # Calculation totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    extra_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Payment Info
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    bank_account_details = models.TextField(blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    payment_notes = models.TextField(blank=True, null=True)
    
    # Extra
    notes = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoices'
        ordering = ['-invoice_date', '-created_at']

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'invoice_items'

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.product_name}"

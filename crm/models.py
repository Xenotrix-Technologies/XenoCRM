from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=100, default='Sales Executive')
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

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
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    alt_phone_number = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255)
    score = models.IntegerField(default=50) # Lead score 0-100
    status = models.CharField(max_length=50, default='New')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='New')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_leads')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    lifecycle_stage = models.CharField(max_length=100, default='Prospect')
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    health_score = models.IntegerField(default=50)
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    last_followup_date_time = models.DateTimeField(blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leads'

    @property
    def status_badge_style(self):
        try:
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
        }
        hex_val = color_map.get(self.status, '#0053db')
        return f"background-color: {hex_val}1a; color: {hex_val}; border: 1px solid {hex_val}33;"

    @property
    def status_badge_class(self):
        if hasattr(self, '_badge_class'):
            return self._badge_class
        try:
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

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, default='Project Task')
    description = models.TextField(blank=True, null=True)
    assignees = models.ManyToManyField(UserProfile, blank=True, related_name='assigned_tasks')
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')

    class Meta:
        db_table = 'events'

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"


class StaffRole(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff_roles')
    name = models.CharField(max_length=100)

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
    status = models.CharField(max_length=50, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agreements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agreement_number} - {self.client_name}"


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



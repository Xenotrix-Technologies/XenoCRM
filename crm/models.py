from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=100, default='Sales Executive')
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

class LeadStatus(models.Model):
    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('grey', 'Grey'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue')
    position = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']

    def __str__(self):
        return self.name

    @property
    def badge_class(self):
        if self.color == 'blue':
            return 'bg-primary-container/10 text-primary border border-primary/20'
        elif self.color == 'grey':
            return 'bg-surface-variant text-on-surface-variant border border-outline-variant/30'
        elif self.color == 'green':
            return 'bg-tertiary-container/20 text-tertiary border border-tertiary/20'
        elif self.color == 'yellow':
            return 'bg-amber-100 text-amber-800 border border-amber-200'
        elif self.color == 'red':
            return 'bg-error-container/40 text-error border border-error/20'
        return 'bg-primary-container/10 text-primary border border-primary/20'


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
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_leads')
    lifecycle_stage = models.CharField(max_length=100, default='Prospect')
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    health_score = models.IntegerField(default=50)
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    last_followup_date_time = models.DateTimeField(blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.type} on {self.lead.name} at {self.timestamp}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({'Completed' if self.completed else 'Pending'})"

class Meeting(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='meetings')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings')
    title = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255, default='Zoom')

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

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"


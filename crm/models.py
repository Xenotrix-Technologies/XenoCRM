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
    company = models.CharField(max_length=255)
    score = models.IntegerField(default=50) # Lead score 0-100
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='New')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_leads')
    lifecycle_stage = models.CharField(max_length=100, default='Prospect')
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    health_score = models.IntegerField(default=50)
    profile_image_url = models.URLField(max_length=1000, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

class BillingPlan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(BillingPlan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default='active')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile} - {self.plan.name} ({self.status})"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body_html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HelpArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

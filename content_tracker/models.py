from django.db import models
from django.contrib.auth.models import User

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

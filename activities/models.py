from django.db import models
from django.contrib.auth.models import User

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
    color = models.CharField(max_length=50, default='#004ac6')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')

    class Meta:
        db_table = 'events'

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"

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

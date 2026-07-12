from django.db import models
from django.contrib.auth.models import User

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

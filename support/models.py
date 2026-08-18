from django.db import models
from core.models import Organization, UserProfile


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


class TicketStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ticket_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'ticket_statuses'

    def __str__(self):
        return self.name


class PriorityStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='priority_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'priority_statuses'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tickets')
    ticket_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Open')
    priority = models.CharField(max_length=50, default='Medium')
    assignee = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    project = models.ForeignKey('activities.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"

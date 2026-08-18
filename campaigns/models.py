from django.db import models
from core.models import Organization, StatusStyleMixin


class CampaignStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaign_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'campaign_statuses'

    def __str__(self):
        return self.name


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Paused', 'Paused'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    is_active = models.BooleanField(default=True)
    
    # Meta Ads Metrics
    results_count = models.IntegerField(default=0)
    results_type = models.CharField(max_length=100, default='Messaging conversations')
    cost_per_result = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_type = models.CharField(max_length=50, default='Lifetime')
    spend = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Meta GST Tax Tracking
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    impressions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    end_date = models.DateField(null=True, blank=True)
    
    platform = models.CharField(max_length=100, default='Meta Ads')
    cost_center = models.CharField(max_length=255, blank=True, null=True)
    leads_generated = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campaigns'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def effective_results(self):
        return self.results_count if self.results_count > 0 else self.leads_generated

    @property
    def calc_cost_per_result(self):
        if self.cost_per_result and float(self.cost_per_result) > 0:
            return float(self.cost_per_result)
        res = self.effective_results
        if res > 0 and self.spend:
            return round(float(self.spend) / float(res), 2)
        return 0.00

    @property
    def calc_gst_amount(self):
        if self.gst_amount and float(self.gst_amount) > 0:
            return float(self.gst_amount)
        if self.spend and float(self.spend) > 0:
            rate = float(self.gst_percentage or 18.00) / 100.0
            return round(float(self.spend) * rate, 2)
        return 0.00

    @property
    def total_spend_with_gst(self):
        return round(float(self.spend or 0.0) + self.calc_gst_amount, 2)

    @property
    def calc_cost_per_result_with_gst(self):
        res = self.effective_results
        if res > 0 and self.total_spend_with_gst:
            return round(float(self.total_spend_with_gst) / float(res), 2)
        return 0.00

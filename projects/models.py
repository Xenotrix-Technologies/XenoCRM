from django.db import models
from django.contrib.auth.models import User

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

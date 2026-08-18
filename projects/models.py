from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from core.models import Organization, StatusStyleMixin


class ClientStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='client_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'client_statuses'

    def __str__(self):
        return self.name


class ProjectStatus(models.Model, StatusStyleMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='project_statuses')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#64748b')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['position', 'id']
        db_table = 'project_statuses'

    def __str__(self):
        return self.name


class Agreement(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Viewed', 'Viewed'),
        ('Pending Signature', 'Pending Signature'),
        ('Signed', 'Signed'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Terminated', 'Terminated'),
        ('Cancelled', 'Cancelled'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='agreements')
    agreement_number = models.CharField(max_length=50, unique=True)
    quotation = models.ForeignKey('finance.Quotation', on_delete=models.SET_NULL, null=True, blank=True, related_name='agreements')
    lead = models.ForeignKey('leads.Lead', on_delete=models.SET_NULL, null=True, blank=True, related_name='agreements')
    
    date = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    
    client_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)
    client_phone = models.CharField(max_length=50, blank=True, null=True)
    client_address = models.TextField(blank=True, null=True)
    gstin = models.CharField(max_length=50, blank=True, null=True)
    
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='agreements')
    agreement_type = models.CharField(max_length=100, default='Website Development Agreement')
    project_name = models.CharField(max_length=255, blank=True, null=True)
    
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    advance_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_cycle = models.CharField(max_length=100, default='Monthly')
    payment_method = models.CharField(max_length=100, default='Bank Transfer')
    
    scope_of_work = models.TextField(blank=True, null=True)
    deliverables_text = models.TextField(blank=True, null=True)
    project_timeline = models.TextField(blank=True, null=True)
    payment_terms_text = models.TextField(blank=True, null=True)
    client_responsibilities_text = models.TextField(blank=True, null=True)
    provider_responsibilities_text = models.TextField(blank=True, null=True)
    confidentiality_clause = models.TextField(blank=True, null=True)
    ip_clause = models.TextField(blank=True, null=True)
    termination_clause = models.TextField(blank=True, null=True)
    refund_policy = models.TextField(blank=True, null=True)
    limitation_liability = models.TextField(blank=True, null=True)
    dispute_resolution = models.TextField(blank=True, null=True)
    governing_law = models.TextField(blank=True, null=True, default='Laws of Telangana, India')
    
    posts_count = models.IntegerField(default=0)
    campaigns_count = models.IntegerField(default=0)
    revisions = models.IntegerField(default=3)
    notice_period = models.IntegerField(default=30)
    notes = models.TextField(blank=True, null=True)
    project_estimation_json = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    public_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    version = models.IntegerField(default=1)

    signature_type = models.CharField(max_length=50, blank=True, null=True)
    signature_data = models.TextField(blank=True, null=True)
    signed_at = models.DateTimeField(blank=True, null=True)
    signed_by_name = models.CharField(max_length=255, blank=True, null=True)
    signed_by_email = models.EmailField(blank=True, null=True)
    signed_ip = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agreements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agreement_number} - {self.client_name}"

    def save(self, *args, **kwargs):
        if not self.public_token:
            self.public_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    @property
    def parsed_estimation(self):
        import json
        if self.project_estimation_json:
            try:
                return json.loads(self.project_estimation_json)
            except Exception:
                pass
        return None


class AgreementVersion(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    snapshot_json = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    change_summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agreement_versions'
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.agreement.agreement_number} v{self.version_number}"


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

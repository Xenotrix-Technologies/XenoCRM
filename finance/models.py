from django.db import models
from django.contrib.auth.models import User

class FinancePaymentMethod(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_payment_methods')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinanceExpenseCategory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_expense_categories')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinancePaymentStatus(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_payment_statuses')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FinanceCommissionType(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='finance_commission_types')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Income(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='incomes')
    date = models.DateField()
    client_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incomes'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.amount}"

class Expense(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.ForeignKey(FinanceExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cost_center = models.CharField(max_length=150, blank=True, null=True)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount}"

class PartnerPayout(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='partner_payouts')
    payout_id = models.CharField(max_length=50)
    partner_name = models.CharField(max_length=255)
    project_client = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.ForeignKey(FinancePaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(FinancePaymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    commission_type = models.ForeignKey(FinanceCommissionType, on_delete=models.SET_NULL, null=True, blank=True)
    payout_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partner_payouts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payout_id} - {self.partner_name} - {self.status}"

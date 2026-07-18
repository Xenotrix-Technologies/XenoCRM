from django.db import models
from crm.models import UserProfile, Organization, Department

class Designation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='designations')
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'hr_designations'
        
    def __str__(self):
        return self.name

class EmployeeProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='employee_profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employee_profiles')
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    date_of_joining = models.DateField(blank=True, null=True)
    salary_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bank_account_details = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'hr_employee_profiles'

    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.job_title}"


class LeaveType(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leave_types')
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_leave_types'
        
    def __str__(self):
        return self.name

class AttendanceStatus(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='attendance_statuses')
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_attendance_statuses'
        
    def __str__(self):
        return self.name

class PayrollRule(models.Model):
    RULE_TYPES = (
        ('Bonus', 'Bonus'),
        ('Deduction', 'Deduction')
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='payroll_rules')
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_percentage = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'hr_payroll_rules'
        
    def __str__(self):
        return f"{self.name} ({self.rule_type})"

class Attendance(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='attendance_logs')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='attendance_logs')
    date = models.DateField()
    clock_in = models.TimeField(blank=True, null=True)
    clock_out = models.TimeField(blank=True, null=True)
    status = models.ForeignKey(AttendanceStatus, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'hr_attendance'
        unique_together = ('user_profile', 'date')

    def __str__(self):
        status_name = self.status.name if self.status else "Unknown"
        return f"{self.user_profile.user.get_full_name()} - {self.date} ({status_name})"


class LeaveRequestStatus(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leave_request_statuses')
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_leave_request_statuses'
        
    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leave_requests')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.ForeignKey(LeaveRequestStatus, on_delete=models.SET_NULL, null=True, blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_leave_requests'
        ordering = ['-applied_on']

    def __str__(self):
        leave_name = self.leave_type.name if self.leave_type else "Unknown"
        status_name = self.status.name if self.status else "Unknown"
        return f"{self.user_profile.user.get_full_name()} - {leave_name} ({status_name})"


class Payroll(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Processed', 'Processed'),
        ('Paid', 'Paid'),
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payrolls')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='payrolls')
    cycle_start_date = models.DateField()
    cycle_end_date = models.DateField()
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bonuses = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    processed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_payrolls'
        ordering = ['-processed_on']

    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.cycle_start_date} to {self.cycle_end_date}"

from django import forms
from .models import EmployeeProfile, Attendance, LeaveRequest, Payroll, LeaveType, AttendanceStatus, PayrollRule, LeaveRequestStatus

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['user_profile', 'employee_id', 'job_title', 'date_of_joining', 'salary_amount', 'bank_account_details']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'bank_account_details': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['user_profile'].queryset = self.fields['user_profile'].queryset.filter(organization=org)
            
        # Add Tailwind classes
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            })


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user_profile', 'date', 'clock_in', 'clock_out', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'clock_in': forms.TimeInput(attrs={'type': 'time'}),
            'clock_out': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['user_profile'].queryset = self.fields['user_profile'].queryset.filter(organization=org)
            
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            })


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['user_profile', 'leave_type', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['user_profile'].queryset = self.fields['user_profile'].queryset.filter(organization=org)
            
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            })


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['user_profile', 'cycle_start_date', 'cycle_end_date', 'base_salary', 'bonuses', 'deductions', 'net_pay', 'status']
        widgets = {
            'cycle_start_date': forms.DateInput(attrs={'type': 'date'}),
            'cycle_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['user_profile'].queryset = self.fields['user_profile'].queryset.filter(organization=org)
            
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
            })


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
                })


class AttendanceStatusForm(forms.ModelForm):
    class Meta:
        model = AttendanceStatus
        fields = ['name', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
                })


class PayrollRuleForm(forms.ModelForm):
    class Meta:
        model = PayrollRule
        fields = ['name', 'rule_type', 'amount', 'is_percentage']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
                })

class LeaveRequestStatusForm(forms.ModelForm):
    class Meta:
        model = LeaveRequestStatus
        fields = ['name', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all'
                })

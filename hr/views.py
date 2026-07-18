from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crm.views import page_permission_required
from crm.models import Department
from .models import EmployeeProfile, Attendance, LeaveRequest, Payroll, LeaveType, AttendanceStatus, PayrollRule, LeaveRequestStatus, Designation
from .forms import EmployeeProfileForm, AttendanceForm, LeaveRequestForm, PayrollForm, LeaveTypeForm, AttendanceStatusForm, PayrollRuleForm, LeaveRequestStatusForm, DepartmentForm, DesignationForm

@login_required
@page_permission_required('hr')
def hr_dashboard(request):
    """
    Main dashboard for Human Resources department.
    """
    org = request.user.profile.organization
    employees_count = EmployeeProfile.objects.filter(organization=org).count()
    # Simple dashboard context for now
    return render(request, 'hr_dashboard.html', {
        'page_title': 'Human Resources',
        'employees_count': employees_count,
    })

@login_required
@page_permission_required('hr')
def hr_employees(request):
    org = request.user.profile.organization
    
    employees = EmployeeProfile.objects.filter(organization=org)
    
    return render(request, 'hr_employees.html', {
        'page_title': 'Employee Directory',
        'employees': employees,
    })

@login_required
@page_permission_required('hr')
def add_employee(request):
    org = request.user.profile.organization
    
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, organization=org)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.organization = org
            employee.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('hr_employees')
    else:
        form = EmployeeProfileForm(organization=org)
        
    return render(request, 'hr_add_employee.html', {
        'page_title': 'Add Employee',
        'form': form
    })

@login_required
@page_permission_required('hr')
def hr_attendance(request):
    org = request.user.profile.organization
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, organization=org)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.organization = org
            attendance.save()
            messages.success(request, 'Attendance logged successfully.')
            return redirect('hr_attendance')
    else:
        form = AttendanceForm(organization=org)
        
    attendances = Attendance.objects.filter(organization=org).order_by('-date')
    
    return render(request, 'hr_attendance.html', {
        'page_title': 'Attendance Tracking',
        'attendances': attendances,
        'form': form
    })

@login_required
@page_permission_required('hr')
def hr_leaves(request):
    org = request.user.profile.organization
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, organization=org)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.organization = org
            leave.save()
            messages.success(request, 'Leave request added successfully.')
            return redirect('hr_leaves')
    else:
        form = LeaveRequestForm(organization=org)
        
    leaves = LeaveRequest.objects.filter(organization=org)
    
    return render(request, 'hr_leaves.html', {
        'page_title': 'Leave Management',
        'leaves': leaves,
        'form': form
    })

@login_required
@page_permission_required('hr')
def hr_payroll(request):
    org = request.user.profile.organization
    
    if request.method == 'POST':
        form = PayrollForm(request.POST, organization=org)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.organization = org
            payroll.save()
            messages.success(request, 'Payroll processed successfully.')
            return redirect('hr_payroll')
    else:
        form = PayrollForm(organization=org)
        
    payrolls = Payroll.objects.filter(organization=org)
    
    return render(request, 'hr_payroll.html', {
        'page_title': 'Payroll Processing',
        'payrolls': payrolls,
        'form': form
    })

@login_required
@page_permission_required('hr')
def hr_settings(request):
    """
    Settings page for HR module to manage statuses and configurations.
    """
    org = request.user.profile.organization
    
    # Forms
    leave_form = LeaveTypeForm()
    attendance_form = AttendanceStatusForm()
    payroll_rule_form = PayrollRuleForm()
    leave_request_status_form = LeaveRequestStatusForm()
    department_form = DepartmentForm()
    designation_form = DesignationForm()
    
    # Handle POST
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_leave_type':
            leave_form = LeaveTypeForm(request.POST)
            if leave_form.is_valid():
                obj = leave_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Leave Type added successfully.')
                return redirect('hr_settings')
                
        elif action == 'add_leave_request_status':
            leave_request_status_form = LeaveRequestStatusForm(request.POST)
            if leave_request_status_form.is_valid():
                obj = leave_request_status_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Leave Request Status added successfully.')
                return redirect('hr_settings')
                
        elif action == 'add_attendance_status':
            attendance_form = AttendanceStatusForm(request.POST)
            if attendance_form.is_valid():
                obj = attendance_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Attendance Status added successfully.')
                return redirect('hr_settings')
                
        elif action == 'add_payroll_rule':
            payroll_rule_form = PayrollRuleForm(request.POST)
            if payroll_rule_form.is_valid():
                obj = payroll_rule_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Payroll Rule added successfully.')
                return redirect('hr_settings')
                
        elif action == 'delete_leave_type':
            item_id = request.POST.get('item_id')
            LeaveType.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Leave Type deleted.')
            return redirect('hr_settings')
            
        elif action == 'delete_leave_request_status':
            item_id = request.POST.get('item_id')
            LeaveRequestStatus.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Leave Request Status deleted.')
            return redirect('hr_settings')
            
        elif action == 'delete_attendance_status':
            item_id = request.POST.get('item_id')
            AttendanceStatus.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Attendance Status deleted.')
            return redirect('hr_settings')
            
        elif action == 'delete_payroll_rule':
            item_id = request.POST.get('item_id')
            PayrollRule.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Payroll Rule deleted.')
            return redirect('hr_settings')
            
        elif action == 'add_department':
            department_form = DepartmentForm(request.POST)
            if department_form.is_valid():
                obj = department_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Department added successfully.')
                return redirect('hr_settings')
                
        elif action == 'delete_department':
            item_id = request.POST.get('item_id')
            Department.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Department deleted.')
            return redirect('hr_settings')
            
        elif action == 'add_designation':
            designation_form = DesignationForm(request.POST)
            if designation_form.is_valid():
                obj = designation_form.save(commit=False)
                obj.organization = org
                obj.save()
                messages.success(request, 'Designation added successfully.')
                return redirect('hr_settings')
                
        elif action == 'delete_designation':
            item_id = request.POST.get('item_id')
            Designation.objects.filter(id=item_id, organization=org).delete()
            messages.success(request, 'Designation deleted.')
            return redirect('hr_settings')

    # Querysets
    leave_types = LeaveType.objects.filter(organization=org)
    attendance_statuses = AttendanceStatus.objects.filter(organization=org)
    payroll_rules = PayrollRule.objects.filter(organization=org)
    leave_request_statuses = LeaveRequestStatus.objects.filter(organization=org)
    departments = Department.objects.filter(organization=org)
    designations = Designation.objects.filter(organization=org)

    return render(request, 'hr_settings.html', {
        'page_title': 'HR Settings',
        'leave_types': leave_types,
        'attendance_statuses': attendance_statuses,
        'payroll_rules': payroll_rules,
        'leave_request_statuses': leave_request_statuses,
        'departments': departments,
        'designations': designations,
        'leave_form': leave_form,
        'attendance_form': attendance_form,
        'payroll_rule_form': payroll_rule_form,
        'leave_request_status_form': leave_request_status_form,
        'department_form': department_form,
        'designation_form': designation_form,
    })

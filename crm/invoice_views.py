import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from .models import Organization, Invoice, InvoiceItem, UserProfile, InvoiceStatus
from .views import get_or_create_dynamic_statuses
import datetime
from django.utils import timezone

@login_required
def invoice_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    organization = user_profile.organization
    
    invoices = Invoice.objects.filter(organization=organization).order_by('-invoice_date')
    
    # Calculate stats using case-insensitive matching
    total_invoices = invoices.count()
    paid_invoices = invoices.filter(status__iexact='Paid').count()
    pending_invoices = invoices.filter(
        Q(status__iexact='Pending') | Q(status__iexact='Draft') | Q(status__iexact='Partial') | Q(status__iexact='Unpaid')
    ).count()
    overdue_invoices = invoices.filter(status__iexact='Overdue').count()
    
    # Simple monthly revenue for current month
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_revenue = invoices.filter(status__iexact='Paid', invoice_date__year=current_year, invoice_date__month=current_month).aggregate(total=Sum('grand_total'))['total'] or 0.00
    invoice_statuses = get_or_create_dynamic_statuses(organization, 'invoices', InvoiceStatus)
    
    context = {
        'invoices': invoices,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'monthly_revenue': monthly_revenue,
        'profile': user_profile,
        'invoice_statuses': invoice_statuses,
    }
    return render(request, 'finance/invoice_dashboard.html', context)

from django.db import transaction

@login_required
def invoice_create(request):
    user_profile = UserProfile.objects.get(user=request.user)
    organization = user_profile.organization
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            raw_status = data.get('status')
            status_val = raw_status.strip() if raw_status else 'Pending'

            with transaction.atomic():
                # Create Invoice
                invoice = Invoice.objects.create(
                    organization=organization,
                    customer_name=data.get('customer_name', ''),
                    company_name=data.get('company_name', ''),
                    phone_number=data.get('phone_number', ''),
                    email_address=data.get('email_address', ''),
                    billing_address=data.get('billing_address', ''),
                    gst_number=data.get('gst_number', ''),
                    invoice_number=data.get('invoice_number') or f"INV-{Invoice.objects.filter(organization=organization).count() + 1:06d}",
                    invoice_date=data.get('invoice_date') or timezone.now().date(),
                    due_date=data.get('due_date') or timezone.now().date(),
                    status=status_val,
                    currency=data.get('currency', 'USD'),
                    subtotal=float(data.get('subtotal') or 0),
                    total_tax=float(data.get('total_tax') or 0),
                    total_discount=float(data.get('total_discount') or 0),
                    extra_discount=float(data.get('extra_discount') or 0),
                    shipping_charge=float(data.get('shipping_charge') or 0),
                    grand_total=float(data.get('grand_total') or 0),
                    amount_paid=float(data.get('amount_paid') or 0),
                    balance_due=float(data.get('balance_due') or 0),
                    payment_method=data.get('payment_method', ''),
                    bank_account_details=data.get('bank_account_details', ''),
                    upi_id=data.get('upi_id', ''),
                    payment_notes=data.get('payment_notes', ''),
                    notes=data.get('notes', ''),
                    terms_conditions=data.get('terms_conditions', '')
                )
                
                # Create Items
                items = data.get('items', [])
                for item in items:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product_name=item.get('product_name', ''),
                        description=item.get('description', ''),
                        quantity=float(item.get('quantity') or 1),
                        unit_price=float(item.get('unit_price') or 0),
                        tax_percentage=float(item.get('tax_percentage') or 0),
                        discount_amount=float(item.get('discount_amount') or 0),
                        line_total=float(item.get('line_total') or 0)
                    )
            
            return JsonResponse({'success': True, 'invoice_id': invoice.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    invoice_count = Invoice.objects.filter(organization=organization).count()
    default_inv_number = f"INV-{invoice_count + 1:06d}"

    invoice_statuses = get_or_create_dynamic_statuses(organization, 'invoices', InvoiceStatus)
    
    return render(request, 'finance/invoice_form.html', {
        'profile': user_profile,
        'default_inv_number': default_inv_number,
        'today': timezone.now().date().isoformat(),
        'invoice_statuses': invoice_statuses,
    })

@login_required
def invoice_detail(request, invoice_id):
    user_profile = UserProfile.objects.get(user=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, organization=user_profile.organization)
    
    return render(request, 'finance/invoice_detail.html', {
        'invoice': invoice,
        'profile': user_profile
    })

@login_required
def invoice_edit(request, invoice_id):
    user_profile = UserProfile.objects.get(user=request.user)
    organization = user_profile.organization
    invoice = get_object_or_404(Invoice, id=invoice_id, organization=organization)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            with transaction.atomic():
                # Update Invoice
                invoice.customer_name = data.get('customer_name', '')
                invoice.company_name = data.get('company_name', '')
                invoice.phone_number = data.get('phone_number', '')
                invoice.email_address = data.get('email_address', '')
                invoice.billing_address = data.get('billing_address', '')
                invoice.gst_number = data.get('gst_number', '')
                invoice.invoice_date = data.get('invoice_date') or invoice.invoice_date
                invoice.due_date = data.get('due_date') or invoice.due_date
                
                raw_status = data.get('status')
                if raw_status:
                    invoice.status = raw_status.strip()
                
                invoice.subtotal = float(data.get('subtotal') or 0)
                invoice.total_tax = float(data.get('total_tax') or 0)
                invoice.total_discount = float(data.get('total_discount') or 0)
                invoice.extra_discount = float(data.get('extra_discount') or 0)
                invoice.shipping_charge = float(data.get('shipping_charge') or 0)
                invoice.grand_total = float(data.get('grand_total') or 0)
                invoice.amount_paid = float(data.get('amount_paid') or 0)
                invoice.balance_due = float(data.get('balance_due') or 0)
                invoice.payment_method = data.get('payment_method', '')
                invoice.bank_account_details = data.get('bank_account_details', '')
                invoice.upi_id = data.get('upi_id', '')
                invoice.payment_notes = data.get('payment_notes', '')
                invoice.notes = data.get('notes', '')
                invoice.terms_conditions = data.get('terms_conditions', '')
                invoice.save()
                
                # Update Items (Delete old, recreate new to handle edits/deletions easily)
                invoice.items.all().delete()
                
                items = data.get('items', [])
                for item in items:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product_name=item.get('product_name', ''),
                        description=item.get('description', ''),
                        quantity=float(item.get('quantity') or 1),
                        unit_price=float(item.get('unit_price') or 0),
                        tax_percentage=float(item.get('tax_percentage') or 0),
                        discount_amount=float(item.get('discount_amount') or 0),
                        line_total=float(item.get('line_total') or 0)
                    )
            
            return JsonResponse({'success': True, 'invoice_id': invoice.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    invoice_statuses = get_or_create_dynamic_statuses(organization, 'invoices', InvoiceStatus)
    
    return render(request, 'finance/invoice_form.html', {
        'profile': user_profile,
        'invoice': invoice,
        'invoice_statuses': invoice_statuses,
    })

@login_required
def invoice_delete(request, invoice_id):
    user_profile = UserProfile.objects.get(user=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, organization=user_profile.organization)
    
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_dashboard')
    
    return redirect('invoice_dashboard')

@login_required
def invoice_update_status(request, invoice_id):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        invoice = get_object_or_404(Invoice, id=invoice_id, organization=user_profile.organization)
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            if new_status:
                invoice.status = new_status.strip()
                invoice.save(update_fields=['status'])
                
                # Recalculate organization stats
                invoices = Invoice.objects.filter(organization=user_profile.organization)
                stats = {
                    'total': invoices.count(),
                    'paid': invoices.filter(status__iexact='Paid').count(),
                    'pending': invoices.filter(
                        Q(status__iexact='Pending') | Q(status__iexact='Draft') | Q(status__iexact='Partial') | Q(status__iexact='Unpaid')
                    ).count(),
                    'overdue': invoices.filter(status__iexact='Overdue').count(),
                }
                return JsonResponse({'success': True, 'stats': stats})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


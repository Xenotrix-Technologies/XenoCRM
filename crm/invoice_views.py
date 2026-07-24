import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from .models import Organization, Invoice, InvoiceItem, UserProfile
import datetime
from django.utils import timezone

@login_required
def invoice_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    organization = user_profile.organization
    
    invoices = Invoice.objects.filter(organization=organization).order_by('-invoice_date')
    
    # Calculate stats
    total_invoices = invoices.count()
    paid_invoices = invoices.filter(status='Paid').count()
    pending_invoices = invoices.filter(status='Pending').count()
    overdue_invoices = invoices.filter(status='Overdue').count()
    
    # Simple monthly revenue for current month
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_revenue = invoices.filter(status='Paid', invoice_date__year=current_year, invoice_date__month=current_month).aggregate(total=Sum('grand_total'))['total'] or 0.00
    
    context = {
        'invoices': invoices,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'monthly_revenue': monthly_revenue,
        'profile': user_profile,
    }
    return render(request, 'finance/invoice_dashboard.html', context)

@login_required
def invoice_create(request):
    user_profile = UserProfile.objects.get(user=request.user)
    organization = user_profile.organization
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create Invoice
            invoice = Invoice.objects.create(
                organization=organization,
                customer_name=data.get('customer_name', ''),
                company_name=data.get('company_name', ''),
                phone_number=data.get('phone_number', ''),
                email_address=data.get('email_address', ''),
                billing_address=data.get('billing_address', ''),
                gst_number=data.get('gst_number', ''),
                invoice_number=data.get('invoice_number', f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"),
                invoice_date=data.get('invoice_date') or timezone.now().date(),
                due_date=data.get('due_date') or timezone.now().date(),
                status=data.get('status', 'Pending'),
                currency=data.get('currency', 'USD'),
                subtotal=data.get('subtotal', 0),
                total_tax=data.get('total_tax', 0),
                total_discount=data.get('total_discount', 0),
                shipping_charge=data.get('shipping_charge', 0),
                grand_total=data.get('grand_total', 0),
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
                    quantity=item.get('quantity', 1),
                    unit_price=item.get('unit_price', 0),
                    tax_percentage=item.get('tax_percentage', 0),
                    discount_percentage=item.get('discount_percentage', 0),
                    line_total=item.get('line_total', 0)
                )
            
            return JsonResponse({'success': True, 'invoice_id': invoice.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    default_inv_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    return render(request, 'finance/invoice_form.html', {
        'profile': user_profile,
        'default_inv_number': default_inv_number,
        'today': timezone.now().date().isoformat()
    })

@login_required
def invoice_detail(request, invoice_id):
    user_profile = UserProfile.objects.get(user=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, organization=user_profile.organization)
    
    return render(request, 'finance/invoice_detail.html', {
        'invoice': invoice,
        'profile': user_profile
    })

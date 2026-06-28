import os

file_path = r'c:\Users\admin\OneDrive\Documents\GitHub\XenoCRM\crm\views.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace XTC-003, XTC-002, XTC-001
content = content.replace('ticket_id="TCK-102"', 'ticket_id="XTC-003"')
content = content.replace('ticket_id="TCK-101"', 'ticket_id="XTC-002"')
content = content.replace('ticket_id="TCK-099"', 'ticket_id="XTC-001"')

# 2. Replace the ticket ID generation
content = content.replace('ticket_id = f"TCK-{100 + ticket_count + 1}"', 'ticket_id = f"XTC-{ticket_count + 1:03d}"')

# 3. Replace Agreement generation
content = content.replace('agreement_number = f"AGR-{year}-{1000 + count + 1}"', 'agreement_number = f"AGR-{year}-{count + 1:03d}"')

# 4. Append Editor Board View
editor_board_code = """
import json
from django.http import JsonResponse

@login_required
def editor_board_view(request):
    org = request.user.profile.organization
    from crm.models import ContentItem
    from django.utils import timezone
    
    today = timezone.now().date()
    items = ContentItem.objects.filter(
        organization=org,
        due_date__year=today.year,
        due_date__month=today.month,
        status__in=['Pending', 'Editing']
    )
    
    priority_filter = request.GET.get('priority_filter', '').strip()
    if priority_filter:
        items = items.filter(priority=priority_filter)
        
    items = items.order_by('-due_date', '-created_at')
    
    current_month_name = today.strftime('%B %Y')
    grouped_items = {current_month_name: list(items)}
    
    status_choices = ['Pending', 'Editing', 'Review']
    
    context = {
        'grouped_items': grouped_items,
        'status_choices': status_choices,
        'priority_filter': priority_filter,
    }
    return render(request, 'editor_board.html', context)

@login_required
def editor_board_update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            status = data.get('status')
            notes = data.get('notes')
            
            org = request.user.profile.organization
            from crm.models import ContentItem
            item = ContentItem.objects.get(id=item_id, organization=org)
            
            if status is not None:
                item.status = status
            if notes is not None:
                item.notes = notes
                
            item.save()
            return JsonResponse({'success': True, 'message': 'Updated successfully.'})
            
        except ContentItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
            
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
"""

if "def editor_board_view" not in content:
    content += editor_board_code

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully.")

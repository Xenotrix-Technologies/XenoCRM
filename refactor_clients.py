import re
import os

path = os.path.join("crm", "views.py")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. clients_view
content = content.replace(
    "leads = Lead.objects.filter(organization=org, status='Qualified')",
    "leads = Lead.objects.filter(organization=org, is_client=True)"
)

# 2. leads_view (around line 895-940)
content = content.replace(
    "leads_export = Lead.objects.filter(organization=org).exclude(status='Qualified')",
    "leads_export = Lead.objects.filter(organization=org, is_client=False)"
)
content = content.replace(
    "leads_qs = Lead.objects.filter(organization=org).exclude(status='Qualified')",
    "leads_qs = Lead.objects.filter(organization=org, is_client=False)"
)

# 3. pipeline_view (around line 1006)
content = content.replace(
    "leads_qs = Lead.objects.filter(organization=org)",
    "leads_qs = Lead.objects.filter(organization=org, is_client=False)"
)

# 4. update_lead_stage (around line 1056)
old_stage_logic = """            elif stage == 'Won':
                lead.status = 'Qualified'
            lead.save()"""

new_stage_logic = """            elif stage == 'Won':
                lead.status = 'Qualified'
                
            if stage == 'Won' or stage == 'Qualified' or lead.status == 'Qualified':
                lead.is_client = True
                from .models import ClientStatus
                status_obj = ClientStatus.objects.filter(organization=org).first()
                lead.status = status_obj.name if status_obj else 'Active'
                
            lead.save()"""
content = content.replace(old_stage_logic, new_stage_logic)

# 5. contact_detail_view (around line 1074)
old_contact_detail = """@login_required
def contact_detail_view(request, lead_id):
    org = request.user.profile.organization
    try:
        lead = Lead.objects.get(id=lead_id, organization=org)
        annotate_lead_badges(lead, org)
    except Lead.DoesNotExist:
        return redirect('leads')"""

new_contact_detail = """@login_required
def contact_detail_view(request, lead_id):
    org = request.user.profile.organization
    try:
        lead = Lead.objects.get(id=lead_id, organization=org)
        if lead.is_client:
            return redirect('client_contact_detail', lead_id=lead.id)
        annotate_lead_badges(lead, org)
    except Lead.DoesNotExist:
        return redirect('leads')"""
content = content.replace(old_contact_detail, new_contact_detail)

# 6. edit_lead (around line 1730)
# we also want edit_lead to mark as client if status == 'Qualified'
old_edit_lead_save = """            lead.save()
            
            Activity.objects.create(
                lead=lead,"""

new_edit_lead_save = """            if lead.status == 'Qualified' and not lead.is_client:
                lead.is_client = True
                from .models import ClientStatus
                status_obj = ClientStatus.objects.filter(organization=org).first()
                lead.status = status_obj.name if status_obj else 'Active'
                
            lead.save()
            
            Activity.objects.create(
                lead=lead,"""
content = content.replace(old_edit_lead_save, new_edit_lead_save)

old_edit_lead_redirect = """            if lead.status == 'Qualified':
                return redirect('clients')
            return redirect('leads')"""

new_edit_lead_redirect = """            if lead.is_client:
                return redirect('client_contact_detail', lead_id=lead.id)
            return redirect('contact_detail', lead_id=lead.id)"""
content = content.replace(old_edit_lead_redirect, new_edit_lead_redirect)

# Add client_contact_detail_view
client_contact_detail_code = """
@login_required
def client_contact_detail_view(request, lead_id):
    org = request.user.profile.organization
    try:
        lead = Lead.objects.get(id=lead_id, organization=org, is_client=True)
        # Assuming ClientStatus objects have similar badge generation or it's handled in the template
    except Lead.DoesNotExist:
        return redirect('clients')
        
    activities = lead.activities.all().order_by('-timestamp')
    tasks = lead.tasks.all().order_by('-created_at')
    owners = UserProfile.objects.filter(organization=org)
    client_statuses = get_or_create_dynamic_statuses(org, 'clients', ClientStatus)
    services = Service.objects.filter(organization=org)
    
    context = {
        'lead': lead,
        'activities': activities,
        'tasks': tasks,
        'owners': owners,
        'client_statuses': client_statuses,
        'services': services,
    }
    return render(request, 'client_contact_detail.html', context)
"""

if "def client_contact_detail_view" not in content:
    content += client_contact_detail_code

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied to views.py successfully.")

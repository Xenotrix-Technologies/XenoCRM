import re
import os

path = os.path.join("crm", "views.py")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# In leads_view, calculating leads_per_service
content = content.replace(
    "leads_qs.filter(service=s).count()",
    "leads_qs.filter(services=s).count()"
)

# In service_clients_view, filtering leads
content = content.replace(
    "leads = leads.filter(service__isnull=True)",
    "leads = leads.filter(services__isnull=True)"
)
content = content.replace(
    "leads = leads.filter(service=service)",
    "leads = leads.filter(services=service)"
)

# In clients_view, collecting service_ids
# Old:
# if lead.service:
#     clients_dict[comp]['service_ids'].add(lead.service.id)
# else:
#     clients_dict[comp]['service_ids'].add(0)

# New:
old_service_ids = """        if lead.service:
            clients_dict[comp]['service_ids'].add(lead.service.id)
        else:
            clients_dict[comp]['service_ids'].add(0)"""
new_service_ids = """        lead_services = lead.services.all()
        if lead_services.exists():
            for s in lead_services:
                clients_dict[comp]['service_ids'].add(s.id)
        else:
            clients_dict[comp]['service_ids'].add(0)"""
content = content.replace(old_service_ids, new_service_ids)

# In create_lead_api:
old_create_lead = """            service_id = request.POST.get('service')
            if service_id:
                try:
                    lead.service = Service.objects.get(id=service_id, organization=org)
                except Service.DoesNotExist:
                    lead.service = None
            lead.save()"""
new_create_lead = """            lead.save()
            service_ids = request.POST.getlist('services')
            if service_ids:
                services = Service.objects.filter(id__in=service_ids, organization=org)
                lead.services.set(services)"""
content = content.replace(old_create_lead, new_create_lead)

# In quick_create_lead:
old_quick_create = """            service_id = request.POST.get('service')
            if service_id:
                try:
                    lead.service = Service.objects.get(id=service_id, organization=org)
                except Service.DoesNotExist:
                    pass
            
            lead.save()"""
new_quick_create = """            lead.save()
            service_ids = request.POST.getlist('services')
            if service_ids:
                services = Service.objects.filter(id__in=service_ids, organization=org)
                lead.services.set(services)"""
content = content.replace(old_quick_create, new_quick_create)

# In edit_lead:
old_edit_lead = """            service_id = request.POST.get('service')
            if service_id:
                try:
                    lead.service = Service.objects.get(id=service_id, organization=org)
                except Service.DoesNotExist:
                    lead.service = None
            else:
                lead.service = None
                
            if lead.status == 'Qualified' and not lead.is_client:"""
new_edit_lead = """            if lead.status == 'Qualified' and not lead.is_client:"""
content = content.replace(old_edit_lead, new_edit_lead)

old_edit_lead2 = """            lead.save()
            
            Activity.objects.create("""
new_edit_lead2 = """            lead.save()
            
            service_ids = request.POST.getlist('services')
            if service_ids:
                services = Service.objects.filter(id__in=service_ids, organization=org)
                lead.services.set(services)
            else:
                lead.services.clear()
            
            Activity.objects.create("""
content = content.replace(old_edit_lead2, new_edit_lead2)


with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated views.py")

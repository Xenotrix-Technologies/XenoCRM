from crm.models import Lead, ClientStatus
from django.db.models import Q

def run():
    print("Migrating leads to clients...")
    leads_to_convert = Lead.objects.filter(Q(status='Qualified') | Q(stage='Won'))
    count = 0
    for lead in leads_to_convert:
        lead.is_client = True
        status_obj = ClientStatus.objects.filter(organization=lead.organization).first()
        lead.status = status_obj.name if status_obj else 'Active'
        lead.save()
        count += 1
    print(f"Successfully migrated {count} leads to clients.")

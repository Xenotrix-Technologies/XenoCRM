from crm.models import Lead

def run():
    print("Migrating single services to multiple services...")
    leads = Lead.objects.filter(service__isnull=False)
    count = 0
    for lead in leads:
        lead.services.add(lead.service)
        count += 1
    print(f"Successfully migrated {count} services.")

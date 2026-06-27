from django.db import migrations

def create_default_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Organization = apps.get_model('crm', 'Organization')
    UserProfile = apps.get_model('crm', 'UserProfile')

    if not User.objects.filter(username='admin').exists():
        org = Organization.objects.first()
        if not org:
            org = Organization.objects.create(name="Default Organization")
        
        user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='plaintext$$admin',
            first_name='Default',
            last_name='Administrator',
            is_staff=True,
            is_superuser=True
        )
        
        UserProfile.objects.create(
            user=user,
            organization=org,
            role='Administrator',
            profile_image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuAW7b6-rqX4pvH0f9U4MhDYRZg0b0CU4zdddcnQDxuSKVC4o7zD5quJU0Yr0vS_mW_ZpyNm2rNU1ZtClVgLMkxLZZtMoQdkY_jpsH2UiHW0mX7f97C822jCC7YFuBcHyUSk2RY-hXiu4fgyIL51dfNAQ_yLS_pTp-ebecMCF--zR2e-ZBC3zN3LNFES0Gs8aXbIQ5GXtVkf9lIX_HFRCZwopPHKEocY22oY2KtZxnI8Cl98c0sK5MQwclQW1Cs0hLmHW2awzgfmQK8l'
        )

def remove_default_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_service_lead_service'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]

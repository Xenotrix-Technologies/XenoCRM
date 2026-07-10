import os
import django
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xenocrm.settings')
django.setup()

from crm.models import Organization, Lead, UserProfile, ContentItem
from django.contrib.auth.models import User

def import_data():
    org, _ = Organization.objects.get_or_create(name="Default Organization")

    csv_path = 'Video_content_Tracker.csv'
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found.")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not any(row.values()):
                continue
            
            client_name = row.get('Client', '').strip()
            if not client_name:
                continue

            video_title = row.get('Video Title', '').strip()
            if not video_title:
                continue

            editor_name = row.get('Editor', '').strip()

            # Find or create Lead
            lead, _ = Lead.objects.get_or_create(
                organization=org,
                name=client_name,
                company=client_name,
                defaults={'email': f"{client_name.lower().replace(' ', '')}@example.com", 'status': 'Qualified'}
            )

            # Find or create Editor
            editor_profile = None
            if editor_name:
                user, _ = User.objects.get_or_create(username=editor_name.lower().replace(' ', ''), defaults={'first_name': editor_name})
                editor_profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'organization': org, 'role': 'Editor'})


            # Parse dates
            def parse_date(d_str):
                if not d_str: return None
                try:
                    # format DD-MM-YY or DD-MM-YYYY
                    if len(d_str.split('-')[-1]) == 2:
                        return datetime.strptime(d_str, '%d-%m-%y').date()
                    else:
                        return datetime.strptime(d_str, '%d-%m-%Y').date()
                except ValueError:
                    return None
            
            # Mappings for dropdowns to ensure valid choices
            status_map = {
                'edited': 'Edited',
                'to edit': 'Editing',
                'uploaded': 'Published',
                'published': 'Published'
            }
            raw_status = row.get('Status', '').strip()
            status = status_map.get(raw_status.lower(), 'Pending')

            camp_status_map = {
                'not ready': 'Not Started',
                'finished': 'Completed',
                'not running': 'Paused'
            }
            raw_camp = row.get('Campaign status', '').strip()
            camp_status = camp_status_map.get(raw_camp.lower(), 'Not Started')

            # Create ContentItem
            ContentItem.objects.create(
                organization=org,
                client=lead,
                video_title=video_title,
                editor=editor_profile,
                date_received=parse_date(row.get('Date Received')),
                due_date=parse_date(row.get('Due Date')),
                status=status,
                platform=row.get('Platform', 'Instagram') or 'Instagram',
                upload_date=parse_date(row.get('Upload Date')),
                post_type=row.get('Post Type', 'Reel') or 'Reel',
                campaign_status=camp_status,
                video_link=row.get('Video Link', ''),
                priority=row.get('Priority', 'Medium') or 'Medium',
                notes=row.get('Notes', '')
            )
            print(f"Imported: {video_title}")

if __name__ == '__main__':
    import_data()

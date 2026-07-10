import re
with open('crm/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_urls = '''
    path('statuses/leads/', views.lead_status_settings, name='lead_status_settings'),
    path('statuses/clients/', views.client_status_settings, name='client_status_settings'),
    path('statuses/projects/', views.project_status_settings, name='project_status_settings'),
    path('statuses/campaigns/', views.campaign_status_settings, name='campaign_status_settings'),
    path('statuses/calendar/', views.calendar_status_settings, name='calendar_status_settings'),
    path('statuses/tickets/', views.ticket_status_settings, name='ticket_status_settings'),
    path('statuses/priority/', views.priority_status_settings, name='priority_status_settings'),
'''

# Replace the single lead_statuses url with all of them
content = content.replace(
    "path('statuses/', views.lead_statuses_view, name='lead_statuses'),",
    new_urls
)

with open('crm/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content_html = f.read()

replacements = {
    "{% url 'lead_statuses' %}?tab=clients": "{% url 'client_status_settings' %}",
    "{% url 'lead_statuses' %}?tab=projects": "{% url 'project_status_settings' %}",
    "{% url 'lead_statuses' %}?tab=campaigns": "{% url 'campaign_status_settings' %}",
    "{% url 'lead_statuses' %}?tab=finance": "{% url 'finance_settings' %}", 
    "{% url 'lead_statuses' %}?tab=calendar": "{% url 'calendar_status_settings' %}",
    "{% url 'lead_statuses' %}?tab=tickets": "{% url 'ticket_status_settings' %}",
    "{% url 'lead_statuses' %}?tab=priority": "{% url 'priority_status_settings' %}",
    "{% url 'lead_statuses' %}": "{% url 'lead_status_settings' %}",
}

for old, new in replacements.items():
    content_html = content_html.replace(old, new)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content_html)

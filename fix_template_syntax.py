import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace: or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'leads') 
# with: or request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'leads'
content = content.replace("or (request.resolver_match.url_name", "or request.resolver_match.url_name")
content = content.replace("and request.GET.tab == 'leads')", "and request.GET.tab == 'leads'")
content = content.replace("and request.GET.tab == 'calendar')", "and request.GET.tab == 'calendar'")
content = content.replace("and request.GET.tab == 'clients')", "and request.GET.tab == 'clients'")
content = content.replace("and request.GET.tab == 'tickets')", "and request.GET.tab == 'tickets'")
content = content.replace("and request.GET.tab == 'projects')", "and request.GET.tab == 'projects'")

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template syntax fixed.")

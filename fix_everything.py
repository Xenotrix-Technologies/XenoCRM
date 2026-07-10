import re
import os

# Let's restore from git first to start clean!
os.system('git checkout templates/lead_statuses.html')

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the Navigation Tabs
tabs_start = content.find('<!-- Navigation Tabs -->')
tabs_end = content.find('<!-- Main Content Grid -->')
if tabs_start != -1 and tabs_end != -1:
    content = content[:tabs_start] + content[tabs_end:]

# 2. Add {% with current_tab=request.GET.tab|default:"leads" %}
content = content.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-8">', 
                          '{% with current_tab=request.GET.tab|default:"leads" %}\n        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">')

# 3. Left panels
panels = [
    ('Leads Status List', 'leads'),
    ('Finance Category List', 'finance'),
    ('Clients List', 'clients'),
    ('Projects List', 'projects'),
    ('Campaigns List', 'campaigns'),
    ('Calendar List', 'calendar'),
    ('Tickets List', 'tickets'),
    ('Priority List', 'priority'),
]

for panel, tab in panels:
    marker = f'<!-- {panel} (Server Backed) -->'
    if tab == 'leads':
        cond = f'{{% if current_tab == "{tab}" %}}'
    else:
        cond = f'{{% elif current_tab == "{tab}" %}}'
    
    content = content.replace(marker, f'{cond}\n                {marker}')

# 4. Right column settings
content = content.replace('<!-- Right Column: Settings & Forms -->',
                          '{% endif %}\n            <!-- Right Column: Settings & Forms -->')

# 5. Right column forms
content = content.replace('<!-- Lead Status Form (Server Backed) -->', 
                          '{% if current_tab == "leads" %}\n                <!-- Lead Status Form (Server Backed) -->')

content = content.replace('<!-- Finance Expense Form -->', 
                          '{% elif current_tab == "finance" %}\n                <!-- Finance Expense Form -->')

content = content.replace('<!-- Dynamic Category Form (Server Backed) -->', 
                          '{% elif current_tab in "clients projects campaigns calendar tickets priority" %}\n                <!-- Dynamic Category Form (Server Backed) -->')

# 6. End forms before Helpful Tips
content = content.replace('<!-- Helpful tips -->', '{% endif %}\n            <!-- Helpful tips -->')

# 7. End grid
# Grid ends right before `<!-- Edit Status Modal (Server Backed Leads Status) -->`
content = content.replace('<!-- Edit Status Modal (Server Backed Leads Status) -->',
                          '{% endwith %}\n\n    <!-- Edit Status Modal (Server Backed Leads Status) -->')


# 8. Javascript Refactoring
content = re.sub(r'function switchCategoryTab\(cat\) \{.*?\}\n', '', content, flags=re.DOTALL)
content = re.sub(r'const urlParams = new URLSearchParams.*?switchCategoryTab\(tab\);', '', content, flags=re.DOTALL)
content = content.replace("let currentCategory = 'leads';", "let currentCategory = '{{ request.GET.tab|default:\"leads\" }}';")
content = content.replace('class="category-panel space-y-6 hidden"', 'class="category-panel space-y-6"')
content = content.replace('class="category-panel space-y-3 hidden"', 'class="category-panel space-y-3"')
content = content.replace('class="category-form space-y-4 hidden"', 'class="category-form space-y-4"')


with open('templates/lead_statuses.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored and refactored completely!")

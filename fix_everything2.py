import re
import os

# Restore
os.system('git checkout HEAD templates/lead_statuses.html')

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Navigation Tabs
tabs_start = content.find('<!-- Navigation Tabs -->')
tabs_end = content.find('<!-- Main Content Panels -->')
if tabs_start != -1 and tabs_end != -1:
    content = content[:tabs_start] + content[tabs_end:]

# 2. Add with block
content = content.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-8">', 
                          '{% with current_tab=request.GET.tab|default:"leads" %}\n        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">')


# 3. Left panels
content = content.replace('<!-- Leads Status List (Server Backed) -->', 
                          '{% if current_tab == "leads" %}\n                <!-- Leads Status List (Server Backed) -->')

content = content.replace('<!-- Clients/Projects/Tickets List (localStorage Backed) -->', 
                          '{% elif current_tab in "clients projects campaigns finance" %}\n                <!-- Clients/Projects/Tickets List (localStorage Backed) -->')

content = content.replace('<!-- Quick Add Templates Manager Card (Only visible when category is calendar) -->', 
                          '{% elif current_tab == "calendar" %}\n            <!-- Quick Add Templates Manager Card (Only visible when category is calendar) -->')

content = content.replace('<!-- Priority Manager Card (Only visible when category is projects) -->', 
                          '{% elif current_tab == "priority" %}\n            <!-- Priority Manager Card (Only visible when category is projects) -->')

# Close left panel group before Right Column
content = content.replace('<!-- Right: Actions/Sidebar Form -->',
                          '{% endif %}\n        <!-- Right: Actions/Sidebar Form -->')


# 4. Right panels
content = content.replace('<!-- Lead Status Form (Server Backed) -->', 
                          '{% if current_tab == "leads" %}\n                <!-- Lead Status Form (Server Backed) -->')

content = content.replace('<!-- Dynamic Category Form (localStorage Backed) -->', 
                          '{% elif current_tab in "clients projects campaigns finance" %}\n                <!-- Dynamic Category Form (localStorage Backed) -->')

content = content.replace('<!-- Add Template Card (Only visible when category is calendar) -->', 
                          '{% elif current_tab == "calendar" %}\n            <!-- Add Template Card (Only visible when category is calendar) -->')

content = content.replace('<!-- Create Priority Card (Only visible when category is projects) -->', 
                          '{% elif current_tab == "priority" %}\n            <!-- Create Priority Card (Only visible when category is projects) -->')

# Close right panel group before Helpful Tips
content = content.replace('<!-- Helpful tips -->', '{% endif %}\n            <!-- Helpful tips -->')

# 5. End grid
content = content.replace('<!-- Edit Status Modal (Server Backed Leads Status) -->',
                          '{% endwith %}\n\n    <!-- Edit Status Modal (Server Backed Leads Status) -->')


# 6. JS changes
content = re.sub(r'function switchCategoryTab\(cat\) \{.*?\}\n', '', content, flags=re.DOTALL)
content = re.sub(r'const urlParams = new URLSearchParams.*?switchCategoryTab\(tab\);', '', content, flags=re.DOTALL)
content = content.replace("let currentCategory = 'leads';", "let currentCategory = '{{ request.GET.tab|default:\"leads\" }}';")
content = content.replace('class="category-panel space-y-6 hidden"', 'class="category-panel space-y-6"')
content = content.replace('class="category-panel space-y-3 hidden"', 'class="category-panel space-y-3"')
content = content.replace('class="category-form space-y-4 hidden"', 'class="category-form space-y-4"')

with open('templates/lead_statuses.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done fixing lead_statuses.html")

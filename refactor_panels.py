import os
import re

file_path = 'templates/lead_statuses.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace category panels
content = content.replace('<!-- Leads Status List (Server Backed) -->', '{% if current_tab == "leads" %}\n                <!-- Leads Status List (Server Backed) -->')
content = content.replace('<!-- Finance Category List (Server Backed) -->', '{% elif current_tab == "finance" %}\n                <!-- Finance Category List (Server Backed) -->')
content = content.replace('<!-- Clients List (Server Backed) -->', '{% elif current_tab == "clients" %}\n                <!-- Clients List (Server Backed) -->')
content = content.replace('<!-- Projects List (Server Backed) -->', '{% elif current_tab == "projects" %}\n                <!-- Projects List (Server Backed) -->')
content = content.replace('<!-- Campaigns List (Server Backed) -->', '{% elif current_tab == "campaigns" %}\n                <!-- Campaigns List (Server Backed) -->')
content = content.replace('<!-- Calendar List (Server Backed) -->', '{% elif current_tab == "calendar" %}\n                <!-- Calendar List (Server Backed) -->')
content = content.replace('<!-- Tickets List (Server Backed) -->', '{% elif current_tab == "tickets" %}\n                <!-- Tickets List (Server Backed) -->')
content = content.replace('<!-- Priority List (Server Backed) -->', '{% elif current_tab == "priority" %}\n                <!-- Priority List (Server Backed) -->')

# Now add {% endif %} at the end of the priority panel, right before the right column starts
content = content.replace('<!-- Right Column: Settings & Forms -->', '{% endif %}\n            <!-- Right Column: Settings & Forms -->')


# Now for the forms:
content = content.replace('<!-- Add Leads Status Form -->', '{% if current_tab == "leads" %}\n                <!-- Add Leads Status Form -->')
content = content.replace('<!-- Finance Expense Form -->', '{% elif current_tab == "finance" %}\n                <!-- Finance Expense Form -->')

# Dynamic Category Form is shared!
content = content.replace('<!-- Dynamic Category Form (Server Backed) -->', '{% elif current_tab in "clients projects campaigns calendar tickets priority" %}\n                <!-- Dynamic Category Form (Server Backed) -->')

# Where does the form section end?
# After Dynamic Category form there's probably:
content = content.replace('<!-- Information Card -->', '{% endif %}\n\n                <!-- Information Card -->')


# Also insert `{% with current_tab=request.GET.tab|default:"leads" %}`
content = content.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-8">', '{% with current_tab=request.GET.tab|default:"leads" %}\n        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">')
content = content.replace('<!-- Edit Status Modal (For Leads) -->', '{% endwith %}\n\n    <!-- Edit Status Modal (For Leads) -->')

# Let's save and then we can check.
with open('templates/lead_statuses_refactored.html', 'w', encoding='utf-8') as f:
    f.write(content)

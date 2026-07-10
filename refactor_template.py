import re

file_path = 'templates/lead_statuses.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert `{% with ... %}` at grid start
content = content.replace(
    '<div class="grid grid-cols-1 md:grid-cols-3 gap-8">',
    '{% with current_tab=request.GET.tab|default:"leads" %}\n        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">'
)

# 2. Left side panels - they all have `class="category-panel ..."`
# We can regex replace the start of each panel
content = re.sub(r'(<!-- Leads Status List \(Server Backed\) -->)', r'{% if current_tab == "leads" %}\n                \1', content)
content = re.sub(r'(<!-- Finance Category List \(Server Backed\) -->)', r'{% elif current_tab == "finance" %}\n                \1', content)
content = re.sub(r'(<!-- Clients List \(Server Backed\) -->)', r'{% elif current_tab == "clients" %}\n                \1', content)
content = re.sub(r'(<!-- Projects List \(Server Backed\) -->)', r'{% elif current_tab == "projects" %}\n                \1', content)
content = re.sub(r'(<!-- Campaigns List \(Server Backed\) -->)', r'{% elif current_tab == "campaigns" %}\n                \1', content)
content = re.sub(r'(<!-- Calendar List \(Server Backed\) -->)', r'{% elif current_tab == "calendar" %}\n                \1', content)
content = re.sub(r'(<!-- Tickets List \(Server Backed\) -->)', r'{% elif current_tab == "tickets" %}\n                \1', content)
content = re.sub(r'(<!-- Priority List \(Server Backed\) -->)', r'{% elif current_tab == "priority" %}\n                \1', content)

# 3. Close the left side panel conditional!
# It ends right before the right column div:
#             <!-- Right Column: Settings & Forms -->
#             <div
#                 class="bg-surface-container
content = content.replace(
    '<!-- Right Column: Settings & Forms -->',
    '{% endif %}\n            <!-- Right Column: Settings & Forms -->'
)

# 4. Right side panels (Forms)
# The first form is lead status form. We insert `{% if current_tab == 'leads' %}` before it.
# Wait, let's look for `<form id="add-status-form"`
content = content.replace(
    '<!-- Lead Status Form (Server Backed) -->',
    '{% if current_tab == "leads" %}\n                <!-- Lead Status Form (Server Backed) -->'
)

# The second form is finance
# Let's find `<form id="add-finance-form"`
content = content.replace(
    '<!-- Finance Expense Form -->',
    '{% elif current_tab == "finance" %}\n                <!-- Finance Expense Form -->'
)

# Dynamic category form
content = content.replace(
    '<!-- Dynamic Category Form (Server Backed) -->',
    '{% elif current_tab in "clients projects campaigns calendar tickets" %}\n                <!-- Dynamic Category Form (Server Backed) -->'
)

# Priority form
content = content.replace(
    '<!-- Create Priority Card (Only visible when category is projects) -->',
    '{% elif current_tab == "priority" %}\n            <!-- Create Priority Card (Only visible when category is projects) -->'
)

# 5. Close the right side panel conditional!
# It ends right before `<!-- Helpful tips -->`
content = content.replace(
    '<!-- Helpful tips -->',
    '{% endif %}\n            <!-- Helpful tips -->'
)

# 6. Close the grid `{% endwith %}`!
# The grid ends at `</div>\n    </div>\n\n    <!-- Edit Status Modal (Server Backed Leads Status) -->`
content = content.replace(
    '<!-- Edit Status Modal (Server Backed Leads Status) -->',
    '{% endwith %}\n\n    <!-- Edit Status Modal (Server Backed Leads Status) -->'
)

# Save
with open('templates/lead_statuses_new.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template refactored successfully.")

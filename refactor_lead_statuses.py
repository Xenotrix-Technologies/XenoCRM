import re

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We will insert `{% with current_tab=request.GET.tab|default:'leads' %}` at the top of the grid
grid_start = content.find('<div class="grid grid-cols-1 md:grid-cols-3 gap-8">')
content = content[:grid_start] + '{% with current_tab=request.GET.tab|default:"leads" %}\n' + content[grid_start:]

# 2. Add `{% endif %}` before the end of the grid (where the right column ends)
grid_end = content.find('<!-- Edit Status Modal (For Leads) -->')
# We have to close the {% with %} and {% endif %} properly.
# Actually, it's easier to just do:

panels = {
    'leads': 'category-panel-leads',
    'finance': 'category-panel-finance',
    'clients': 'category-panel-clients',
    'projects': 'category-panel-projects',
    'campaigns': 'category-panel-campaigns',
    'calendar': 'category-panel-calendar',
    'tickets': 'category-panel-tickets',
    'priority': 'category-panel-priority',
}

forms = {
    'leads': 'add-status-form',
    'finance': 'add-finance-form', # wait, what is the ID?
}

# The best way is to wrap EACH panel and EACH form with an `{% if current_tab == '...' %}`
for cat, panel_id in panels.items():
    if cat == 'leads':
        cond = f"{{% if current_tab == '{cat}' %}}"
    else:
        cond = f"{{% if current_tab == '{cat}' %}}"
        
    pattern = rf'(<div id="{panel_id}".*?</div>\s*</div>\s*(?=<!--|$|<div id="category-panel))'
    # Actually, regexing HTML is notoriously hard for nested divs.

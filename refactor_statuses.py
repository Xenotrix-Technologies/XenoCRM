import re

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Navigation Tabs
nav_tabs = r'''    <!-- Navigation Tabs -->\n    <div class="border-b border-outline-variant mb-6 w-full">\n        <nav class="flex gap-4 md:gap-8 overflow-x-auto no-scrollbar">\n[\s\S]*?        </nav>\n    </div>'''
content = re.sub(nav_tabs, '', content)

# 2. Update switchCategoryTab to change header title
switch_func = r'''    function switchCategoryTab\(cat\) \{'''
switch_func_replacement = '''    function switchCategoryTab(cat) {
        // Dynamically update page title
        const titleMap = {
            'leads': 'Leads Status Management',
            'clients': 'Clients Status Management',
            'projects': 'Projects Status Management',
            'campaigns': 'Campaigns Status Management',
            'calendar': 'Calendar Status Management',
            'tickets': 'Ticket Status Management',
            'finance': 'Finance Status Management'
        };
        const h2Title = document.querySelector('h2.text-headline-lg');
        if (h2Title) h2Title.textContent = titleMap[cat] || 'Status Management';
'''
content = re.sub(switch_func, switch_func_replacement, content, count=1)

with open('templates/lead_statuses.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("lead_statuses.html refactored successfully.")

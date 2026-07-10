import re

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove flex-1 empty divs
content = re.sub(r'<div class="flex-1">\s*</div>', '', content)

# Add w-full to status-drag-item and dynamic-drag-item
content = content.replace('class="status-drag-item flex items-center', 'class="status-drag-item w-full flex items-center')
content = content.replace('class="dynamic-drag-item flex items-center', 'class="dynamic-drag-item w-full flex items-center')

with open('templates/lead_statuses.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes applied successfully.")
